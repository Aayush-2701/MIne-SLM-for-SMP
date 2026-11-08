"""
Vector Semantic Retriever implementing Section 3.5.2:
sim(A, B) = (A . B) / (||A|| * ||B||)
Supports dense semantic embeddings with FAISS vector index and normalized cosine similarity.
"""
import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
import faiss

class VectorRetriever:
    def __init__(self, chunks: List[Dict[str, Any]], embedding_dim: int = 256):
        self.chunks = chunks
        self.embedding_dim = embedding_dim
        self.corpus = [f"{c['doc_title']} | {c['section_clause']} | {c['text']}" for c in self.chunks]
        
        # Build dense semantic vector representations
        # Uses word n-grams (1, 2) and char sub-grams (3, 5) to support technical mining compounds & multilingual scripts
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            max_features=4096,
            sublinear_tf=True
        )
        tfidf_matrix = self.vectorizer.fit_transform(self.corpus).toarray().astype('float32')
        
        # Normalize vectors to unit sphere so inner product equals cosine similarity
        norms = np.linalg.norm(tfidf_matrix, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        self.normalized_vectors = tfidf_matrix / norms
        
        # Build FAISS IndexFlatIP (Inner Product on normalized vectors = Cosine Similarity)
        dim = self.normalized_vectors.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(self.normalized_vectors)

    def retrieve(self, query: str, top_k: int = 10) -> List[Tuple[Dict[str, Any], float, int]]:
        """
        Retrieves top_k chunks using dense vector cosine similarity.
        Returns list of tuples: (chunk_dict, cosine_similarity_score, rank_1_based)
        """
        if not query.strip():
            return []
            
        q_vec = self.vectorizer.transform([query]).toarray().astype('float32')
        q_norm = np.linalg.norm(q_vec)
        if q_norm > 0:
            q_vec = q_vec / q_norm
        else:
            return []
            
        distances, indices = self.index.search(q_vec, min(top_k, len(self.chunks)))
        
        results = []
        for rank, (score, idx) in enumerate(zip(distances[0], indices[0]), start=1):
            if idx >= 0 and score > 0.001:
                results.append((self.chunks[idx], float(score), rank))
        return results
