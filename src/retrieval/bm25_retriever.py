"""
BM25 Lexical Retriever implementing Section 3.5.3:
BM25(D, Q) = sum_{q_i in Q} IDF(q_i) * [f(q_i, D) * (k1 + 1)] / [f(q_i, D) + k1 * (1 - b + b * |D| / avgdl)]
Specialized tokenization for mining regulations, clause numbers, and technical terms.
"""
import re
from typing import List, Dict, Any, Tuple
from rank_bm25 import BM25Okapi
from src.config import BM25_K1, BM25_B

def tokenize_mining_text(text: str) -> List[str]:
    """
    Tokenizes text while retaining regulation numbers, abbreviations,
    units (e.g. 500m, 1.25%, 15m), and alphanumeric identifiers.
    """
    cleaned = text.lower()
    # Normalize punctuation but retain hyphens in identifiers (e.g., cmr-2017, deg-iii)
    tokens = re.findall(r'[a-z0-9\u0900-\u097F\u0980-\u09FF\u0B00-\u0B7F\u0C00-\u0C7F\u0C80-\u0CFF\.\-\%]+', cleaned)
    # Strip solitary dots or hyphens
    return [t.strip('.-') for t in tokens if len(t.strip('.-')) > 1]

class BM25Retriever:
    def __init__(self, chunks: List[Dict[str, Any]], k1: float = BM25_K1, b: float = BM25_B):
        self.chunks = chunks
        self.k1 = k1
        self.b = b
        self.corpus = [f"{c['doc_title']} {c['section_clause']} {c['text']}" for c in self.chunks]
        self.tokenized_corpus = [tokenize_mining_text(doc) for doc in self.corpus]
        self.bm25 = BM25Okapi(self.tokenized_corpus, k1=self.k1, b=self.b)

    def retrieve(self, query: str, top_k: int = 10) -> List[Tuple[Dict[str, Any], float, int]]:
        """
        Retrieves top_k chunks using BM25 ranking.
        Returns list of tuples: (chunk_dict, bm25_score, rank_1_based)
        """
        tokenized_query = tokenize_mining_text(query)
        if not tokenized_query:
            return []
            
        scores = self.bm25.get_scores(tokenized_query)
        # Pair chunk with score and index
        ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        
        results = []
        for rank, idx in enumerate(ranked_indices[:top_k], start=1):
            if scores[idx] > 0.0001:  # Only include non-zero matches
                results.append((self.chunks[idx], float(scores[idx]), rank))
        return results
