"""
Unified Hybrid Retrieval Engine (Section 3.3.3 & Figure 3.2, 3.3).
Orchestrates BM25 Lexical Ranking, Dense Vector Cosine Ranking, and RRF Fusion.
"""
from typing import List, Dict, Any, Optional
from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.vector_retriever import VectorRetriever
from src.retrieval.rrf_fusion import ReciprocalRankFusion
from src.config import TOP_K_RETRIEVAL

class HybridRetrievalEngine:
    def __init__(self, chunks: List[Dict[str, Any]]):
        self.chunks = chunks
        self.bm25_retriever = BM25Retriever(chunks)
        self.vector_retriever = VectorRetriever(chunks)
        self.fusion = ReciprocalRankFusion()

    def search(
        self,
        query: str,
        top_k: int = TOP_K_RETRIEVAL,
        filter_doc_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Executes hybrid search:
        1. Query BM25 index -> top 15 candidate passages
        2. Query Dense Vector index -> top 15 candidate passages
        3. Reciprocal Rank Fusion -> top_k fused passages
        4. Optional metadata filtering
        """
        if not query.strip() or not self.chunks:
            return []

        # Retrieve candidates from both pathways
        candidate_pool_size = max(15, top_k * 3)
        bm25_candidates = self.bm25_retriever.retrieve(query, top_k=candidate_pool_size)
        vector_candidates = self.vector_retriever.retrieve(query, top_k=candidate_pool_size)

        # Apply document filter if specified
        if filter_doc_id and filter_doc_id != "ALL":
            bm25_candidates = [item for item in bm25_candidates if item[0]["doc_id"] == filter_doc_id]
            vector_candidates = [item for item in vector_candidates if item[0]["doc_id"] == filter_doc_id]

        # Reciprocal Rank Fusion
        fused_chunks = self.fusion.fuse(bm25_candidates, vector_candidates, top_n=top_k)
        return fused_chunks
