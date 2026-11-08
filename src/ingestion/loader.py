"""
Document Loader and Knowledge Base Indexer.
Supports PyMuPDF for PDF extraction, JSON, Markdown, and custom uploads.
"""
import json
from pathlib import Path
from typing import List, Dict, Any
import fitz # PyMuPDF
from src.config import RAW_DOCS_DIR, PROCESSED_CHUNKS_PATH, DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP
from src.ingestion.chunker import RegulatoryChunker

class DocumentLoader:
    def __init__(self, chunk_size: int = DEFAULT_CHUNK_SIZE, chunk_overlap: int = DEFAULT_CHUNK_OVERLAP):
        self.chunker = RegulatoryChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    def extract_text_from_pdf(self, pdf_path: Path) -> List[Dict[str, Any]]:
        """Extracts text page by page from a PDF using PyMuPDF (fitz) preserving page numbers."""
        pages_data = []
        doc = fitz.open(str(pdf_path))
        doc_name = pdf_path.stem
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")
            if text.strip():
                pages_data.append({
                    "page_number": page_num + 1,
                    "text": text,
                    "doc_title": doc_name.replace("_", " "),
                    "doc_id": doc_name[:25].upper()
                })
        doc.close()
        return pages_data

    def load_all_documents(self) -> List[Dict[str, Any]]:
        """Loads all documents from RAW_DOCS_DIR and generates standardized chunks."""
        chunks: List[Dict[str, Any]] = []
        
        # 1. Load curated JSON database
        json_file = RAW_DOCS_DIR / "dgms_and_mine_plans.json"
        if json_file.exists():
            with open(json_file, "r", encoding="utf-8") as f:
                docs = json.load(f)
                for d in docs:
                    base_meta = {
                        "doc_id": d.get("doc_id", "DOC"),
                        "doc_title": d.get("title", ""),
                        "issuing_authority": d.get("issuing_authority", ""),
                        "publication_date": d.get("publication_date", ""),
                        "revision_status": d.get("status", "Current"),
                        "source_location": d.get("source_location", "")
                    }
                    for sec in d.get("sections", []):
                        sec_meta = dict(base_meta)
                        sec_meta["section_clause"] = sec.get("section", "")
                        sec_meta["page_number"] = sec.get("page", 1)
                        sec_chunks = self.chunker.chunk_section(sec.get("content", ""), sec_meta)
                        chunks.extend(sec_chunks)

        # 2. Check for uploaded / raw PDFs in raw_documents
        for pdf_path in RAW_DOCS_DIR.glob("*.pdf"):
            # Avoid duplicate if it's the generated sample extracts
            if "DGMS_CMR_2017_Official_Extracts" in pdf_path.name:
                continue
            extracted = self.extract_text_from_pdf(pdf_path)
            for page in extracted:
                meta = {
                    "doc_id": page["doc_id"],
                    "doc_title": page["doc_title"],
                    "issuing_authority": "Uploaded Mining Technical Authority",
                    "publication_date": "2026",
                    "revision_status": "Uploaded PDF",
                    "section_clause": f"Page {page['page_number']}",
                    "page_number": page["page_number"],
                    "source_location": str(pdf_path)
                }
                page_chunks = self.chunker.chunk_section(page["text"], meta)
                chunks.extend(page_chunks)

        # Save processed chunks
        with open(PROCESSED_CHUNKS_PATH, "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)

        print(f"[OK] Ingested and created {len(chunks)} regulatory chunks at {PROCESSED_CHUNKS_PATH.name}")
        return chunks

    def process_custom_upload(self, file_bytes: bytes, filename: str, doc_metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Processes an on-the-fly uploaded document (PDF or text/markdown) and adds to chunks."""
        new_chunks = []
        if filename.lower().endswith(".pdf"):
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text("text")
                if text.strip():
                    meta = dict(doc_metadata)
                    meta["page_number"] = page_num + 1
                    meta["section_clause"] = f"Page {page_num + 1}"
                    meta["source_location"] = filename
                    page_chunks = self.chunker.chunk_section(text, meta)
                    new_chunks.extend(page_chunks)
            doc.close()
        else:
            text = file_bytes.decode("utf-8", errors="ignore")
            meta = dict(doc_metadata)
            meta["page_number"] = 1
            meta["section_clause"] = "Full Document"
            meta["source_location"] = filename
            new_chunks = self.chunker.chunk_section(text, meta)

        # Append to existing chunks
        existing = []
        if PROCESSED_CHUNKS_PATH.exists():
            with open(PROCESSED_CHUNKS_PATH, "r", encoding="utf-8") as f:
                existing = json.load(f)
        existing.extend(new_chunks)
        with open(PROCESSED_CHUNKS_PATH, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)
            
        return new_chunks
