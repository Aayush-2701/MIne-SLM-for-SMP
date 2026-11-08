"""
Reciprocal Rank Fusion (RRF) implementing Section 3.5.4 Equation:
RRF(d) = sum_{r in R} 1 / (k + rank_r(d))
Combines BM25 lexical ranking and Vector semantic ranking.
"""
from typing import List, Dict, Any, Tuple
from collections import defaultdict
from src.config import RRF_K

class ReciprocalRankFusion:
    def __init__(self, k: int = RRF_K):
        self.k = k

    def fuse(
        self,
        bm25_results: List[Tuple[Dict[str, Any], float, int]],
        vector_results: List[Tuple[Dict[str, Any], float, int]],
        top_n: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Fuses the candidate lists using RRF.
        Returns a sorted list of chunks with attached fusion metadata:
        - rrf_score
        - bm25_rank & bm25_score
        - vector_rank & vector_score
        - retrieval_source ('hybrid', 'lexical_only', 'vector_only')
        """
        rrf_scores = defaultdict(float)
        chunk_map = {}
        detail_map = defaultdict(lambda: {
            "bm25_rank": None,
            "bm25_score": 0.0,
            "vector_rank": None,
            "vector_score": 0.0
        })

        # Process BM25 ranked list
        for chunk, score, rank in bm25_results:
            cid = chunk["chunk_id"]
            chunk_map[cid] = chunk
            rrf_scores[cid] += 1.0 / (self.k + rank)
            detail_map[cid]["bm25_rank"] = rank
            detail_map[cid]["bm25_score"] = round(score, 4)

        # Process Vector ranked list
        for chunk, score, rank in vector_results:
            cid = chunk["chunk_id"]
            chunk_map[cid] = chunk
            rrf_scores[cid] += 1.0 / (self.k + rank)
            detail_map[cid]["vector_rank"] = rank
            detail_map[cid]["vector_score"] = round(score, 4)

        # Sort by RRF score descending
        sorted_cids = sorted(rrf_scores.keys(), key=lambda c: rrf_scores[c], reverse=True)

        final_ranked = []
        for rank, cid in enumerate(sorted_cids[:top_n], start=1):
            chunk_copy = dict(chunk_map[cid])
            info = detail_map[cid]
            
            if info["bm25_rank"] is not None and info["vector_rank"] is not None:
                source = "Hybrid (BM25 + Dense Vector)"
            elif info["bm25_rank"] is not None:
                source = "BM25 Lexical Exact"
            else:
                source = "Dense Vector Semantic"

            chunk_copy["rrf_rank"] = rank
            chunk_copy["rrf_score"] = round(rrf_scores[cid], 6)
            chunk_copy["bm25_rank"] = info["bm25_rank"]
            chunk_copy["bm25_score"] = info["bm25_score"]
            chunk_copy["vector_rank"] = info["vector_rank"]
            chunk_copy["vector_score"] = info["vector_score"]
            chunk_copy["retrieval_method"] = source
            final_ranked.append(chunk_copy)

        return final_ranked
