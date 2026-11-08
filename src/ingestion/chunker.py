"""
Text Chunking Module implementing Section 3.5.1 Design Calculations:
S = C - O
Associates each chunk with regulatory metadata conforming to Appendix A Table A.1.
"""
import re
from typing import List, Dict, Any
from src.config import DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP

class RegulatoryChunker:
    def __init__(self, chunk_size: int = DEFAULT_CHUNK_SIZE, chunk_overlap: int = DEFAULT_CHUNK_OVERLAP):
        self.chunk_size = chunk_size        # C
        self.chunk_overlap = chunk_overlap  # O
        self.step_size = chunk_size - chunk_overlap # S = C - O
        if self.step_size <= 0:
            raise ValueError(f"Chunk size C ({chunk_size}) must be greater than overlap O ({chunk_overlap})")

    def clean_text(self, text: str) -> str:
        """Removes excessive whitespace and normalization artefacts while preserving structure."""
        text = re.sub(r'\r\n|\r', '\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    def chunk_section(self, text: str, base_metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Splits a document section into chunks using sliding window (S = C - O).
        Preserves complete paragraphs when possible and attaches Table A.1 metadata.
        """
        cleaned = self.clean_text(text)
        words = cleaned.split()
        total_words = len(words)
        
        chunks = []
        if total_words <= self.chunk_size:
            # Entire section fits in one chunk
            chunk_id = f"{base_metadata.get('doc_id', 'DOC')}-SEC-{base_metadata.get('page_number', '1')}-CH-001"
            chunk_entry = {
                "chunk_id": chunk_id,
                "doc_id": base_metadata.get("doc_id", "UNKNOWN"),
                "doc_title": base_metadata.get("doc_title", ""),
                "issuing_authority": base_metadata.get("issuing_authority", ""),
                "publication_date": base_metadata.get("publication_date", ""),
                "revision_status": base_metadata.get("revision_status", "Current"),
                "section_clause": base_metadata.get("section_clause", ""),
                "page_number": base_metadata.get("page_number", 1),
                "source_location": base_metadata.get("source_location", ""),
                "text": cleaned,
                "token_count": len(words),
                "char_length": len(cleaned)
            }
            chunks.append(chunk_entry)
            return chunks

        # Sliding window chunking
        idx = 0
        chunk_num = 1
        while idx < total_words:
            end_idx = min(idx + self.chunk_size, total_words)
            chunk_words = words[idx:end_idx]
            chunk_text = " ".join(chunk_words)
            
            chunk_id = f"{base_metadata.get('doc_id', 'DOC')}-SEC-{base_metadata.get('page_number', '1')}-CH-{chunk_num:03d}"
            chunk_entry = {
                "chunk_id": chunk_id,
                "doc_id": base_metadata.get("doc_id", "UNKNOWN"),
                "doc_title": base_metadata.get("doc_title", ""),
                "issuing_authority": base_metadata.get("issuing_authority", ""),
                "publication_date": base_metadata.get("publication_date", ""),
                "revision_status": base_metadata.get("revision_status", "Current"),
                "section_clause": base_metadata.get("section_clause", ""),
                "page_number": base_metadata.get("page_number", 1),
                "source_location": base_metadata.get("source_location", ""),
                "text": chunk_text,
                "token_count": len(chunk_words),
                "char_length": len(chunk_text)
            }
            chunks.append(chunk_entry)
            
            if end_idx >= total_words:
                break
            idx += self.step_size
            chunk_num += 1

        return chunks
