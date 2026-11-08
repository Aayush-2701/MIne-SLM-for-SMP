"""
Automated Unit and Integration Tests for Mine SLM Platform.
Validates chunking mathematics (S = C - O), BM25, Vector Cosine similarity,
RRF fusion, response grounding, abstention, and SMP generation.
"""
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from src.config import DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP
from src.ingestion.data_builder import build_data_repository
from src.ingestion.chunker import RegulatoryChunker
from src.ingestion.loader import DocumentLoader
from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.vector_retriever import VectorRetriever
from src.retrieval.rrf_fusion import ReciprocalRankFusion
from src.retrieval.hybrid_engine import HybridRetrievalEngine
from src.generation.slm_engine import SLMGenerationEngine
from src.smp_generator.plan_generator import SafetyManagementPlanGenerator
from src.evaluation.benchmark import EvaluationBenchmark

def test_data_repository_and_pdf_creation():
    build_data_repository()
    loader = DocumentLoader()
    chunks = loader.load_all_documents()
    assert len(chunks) > 0, "Chunks list should not be empty"
    print(f"Loaded {len(chunks)} chunks.")

def test_chunking_formula():
    c = 100
    o = 25
    chunker = RegulatoryChunker(chunk_size=c, chunk_overlap=o)
    assert chunker.step_size == 75, "Step size S should equal C - O = 75"
    
    text = " ".join([f"token_{i}" for i in range(250)])
    meta = {"doc_id": "TEST", "page_number": 1, "doc_title": "Test Doc"}
    chunks = chunker.chunk_section(text, meta)
    assert len(chunks) >= 3, f"Expected at least 3 chunks, got {len(chunks)}"

def test_bm25_exact_retrieval():
    loader = DocumentLoader()
    chunks = loader.load_all_documents()
    bm25 = BM25Retriever(chunks)
    
    # Query for exact regulation number
    results = bm25.retrieve("Regulation 104 Safety Management Plan", top_k=3)
    assert len(results) > 0, "BM25 should return results"
    top_chunk, score, rank = results[0]
    assert "Regulation 104" in top_chunk["section_clause"] or "104" in top_chunk["text"]

def test_vector_semantic_retrieval():
    loader = DocumentLoader()
    chunks = loader.load_all_documents()
    vec = VectorRetriever(chunks)
    
    # Conceptually phrased query without exact numbers
    results = vec.retrieve("standards for air quality and airflow in underground tunnels", top_k=3)
    assert len(results) > 0, "Vector retriever should return results"
    top_chunk, score, rank = results[0]
    assert "Ventilation" in top_chunk["section_clause"] or "ventilation" in top_chunk["text"].lower()

def test_rrf_hybrid_fusion():
    loader = DocumentLoader()
    chunks = loader.load_all_documents()
    hybrid = HybridRetrievalEngine(chunks)
    
    fused = hybrid.search("maximum gradient and berm height on haul roads", top_k=3)
    assert len(fused) == 3
    top_c = fused[0]
    assert "Haul Roads" in top_c["section_clause"] or "83" in top_c["section_clause"]
    assert "rrf_score" in top_c
    assert top_c["rrf_score"] > 0

def test_grounded_generation_and_abstention():
    loader = DocumentLoader()
    chunks = loader.load_all_documents()
    hybrid = HybridRetrievalEngine(chunks)
    slm = SLMGenerationEngine()

    # Legitimate mining query
    rel_chunks = hybrid.search("blasting danger zone distance", top_k=3)
    res = slm.generate_response("blasting danger zone distance", rel_chunks, target_lang="en")
    assert res["is_grounded"] is True
    assert res["abstained"] is False
    assert len(res["citations"]) > 0

    # Unrelated query requiring abstention
    irr_chunks = hybrid.search("quantum computer operating system specifications", top_k=3)
    res_abstain = slm.generate_response("quantum computer operating system specifications", irr_chunks, target_lang="en")
    assert res_abstain["abstained"] is True, "System should abstain from unsupported query"

def test_safety_management_plan_generation():
    loader = DocumentLoader()
    chunks = loader.load_all_documents()
    hybrid = HybridRetrievalEngine(chunks)
    smp_gen = SafetyManagementPlanGenerator()
    
    stat_chunks = hybrid.search("Safety Management Plan Regulation 104", top_k=3)
    mine_params = {
        "mine_name": "Gevra Opencast",
        "company": "SECL",
        "mine_type": "Opencast Coal Mine",
        "capacity": "50 MTPA",
        "pit_depth": "120m",
        "workforce": "2,000",
        "manager_name": "Er. Sharma",
        "safety_officer": "Er. Verma"
    }
    plan = smp_gen.generate_plan(mine_params, stat_chunks)
    assert "sections" in plan
    assert len(plan["sections"]) == 10, "Appendix C specifies 10 mandatory sections"
    assert "Regulation 104" in plan["markdown"]

def test_benchmark_suite():
    loader = DocumentLoader()
    chunks = loader.load_all_documents()
    hybrid = HybridRetrievalEngine(chunks)
    slm = SLMGenerationEngine()
    evaluator = EvaluationBenchmark(hybrid, slm)
    
    summary = evaluator.run_benchmark(k=3)
    assert summary["total_queries_evaluated"] > 0
    assert summary["mean_reciprocal_rank_MRR"] > 0.70, f"MRR should be > 0.70, got {summary['mean_reciprocal_rank_MRR']}"
    assert summary["recall_at_k"] > 0.70, f"Recall should be > 0.70, got {summary['recall_at_k']}"
    print(f"Evaluation benchmark passed! MRR: {summary['mean_reciprocal_rank_MRR']}, P@3: {summary['precision_at_k']}")

if __name__ == "__main__":
    test_data_repository_and_pdf_creation()
    test_chunking_formula()
    test_bm25_exact_retrieval()
    test_vector_semantic_retrieval()
    test_rrf_hybrid_fusion()
    test_grounded_generation_and_abstention()
    test_safety_management_plan_generation()
    test_benchmark_suite()
    print("\n[ALL TESTS PASSED SUCCESSFULLY!]")
