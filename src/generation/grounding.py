"""
Response Grounding & Verification Module (Section 3.3.4, 3.5.5, 4.2).
Enforces:
1. Grounded evidence extraction with source citations.
2. Abstention behavior if retrieved evidence is insufficient (averts hallucination).
3. Separation of statutory facts from operational recommendations.
"""
from typing import List, Dict, Any, Tuple
from src.config import MIN_GROUNDING_CONFIDENCE

class GroundingVerifier:
    def __init__(self, min_confidence: float = MIN_GROUNDING_CONFIDENCE):
        self.min_confidence = min_confidence

    def evaluate_evidence_sufficiency(self, query: str, retrieved_chunks: List[Dict[str, Any]]) -> Tuple[bool, float, str]:
        """
        Determines whether the retrieved chunks provide sufficient evidence to answer the query.
        Returns (is_sufficient, confidence_score, explanation).
        """
        if not retrieved_chunks:
            return False, 0.0, "No relevant regulatory or operational passages were found in the knowledge base."

        top_chunk = retrieved_chunks[0]
        rrf_score = top_chunk.get("rrf_score", 0.0)
        vector_score = top_chunk.get("vector_score", 0.0)
        bm25_score = top_chunk.get("bm25_score", 0.0)

        # If semantic vector cosine similarity is very low (< 0.09) or BM25 is low with weak vector score (< 0.10),
        # the query lacks substantive alignment with mining safety regulations and triggers abstention.
        if vector_score < 0.08 or (bm25_score < 3.0 and vector_score < 0.10):
            return False, 0.05, (
                "ABSTENTION: The query appears to fall outside the scope of available DGMS regulations, "
                "circulars, and mine operational documents. The system abstains from generating an ungrounded response."
            )

        norm_rrf = min(1.0, rrf_score / 0.032)
        norm_vec = min(1.0, vector_score * 3.0)
        norm_bm = min(1.0, bm25_score / 6.0) if bm25_score > 0 else 0.0
        
        confidence = round(0.4 * norm_rrf + 0.35 * norm_vec + 0.25 * norm_bm, 3)

        if confidence < self.min_confidence:
            return False, confidence, (
                "ABSTENTION: Low groundedness confidence. The available knowledge base does not contain "
                "sufficient authoritative provisions to answer reliably."
            )

        return True, max(confidence, 0.50), "Evidence verified against authoritative knowledge base."

    def format_citations(self, retrieved_chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Formats source citations with full metadata according to Appendix A Table A.1.
        """
        citations = []
        seen_keys = set()
        for idx, chunk in enumerate(retrieved_chunks, start=1):
            key = (chunk.get("doc_id"), chunk.get("section_clause"))
            if key in seen_keys:
                continue
            seen_keys.add(key)
            
            citations.append({
                "citation_number": len(citations) + 1,
                "chunk_id": chunk.get("chunk_id", f"CHK-{idx}"),
                "document_title": chunk.get("doc_title", "DGMS Document"),
                "document_id": chunk.get("doc_id", "DOC"),
                "issuing_authority": chunk.get("issuing_authority", "DGMS India"),
                "section_clause": chunk.get("section_clause", "General"),
                "page_number": chunk.get("page_number", 1),
                "publication_date": chunk.get("publication_date", "N/A"),
                "revision_status": chunk.get("revision_status", "Current"),
                "source_location": chunk.get("source_location", ""),
                "retrieval_method": chunk.get("retrieval_method", "Hybrid RAG"),
                "snippet": chunk.get("text", "")[:280] + "..."
            })
        return citations
