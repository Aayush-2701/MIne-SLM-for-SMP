"""
Mine SLM for Safety Management Plan
AI-Based Platform Built on Hybrid RAG for Grounded, Multilingual Mine-Safety Information Access for Indian Mines
National Institute of Technology Karnataka, Surathkal - Department of Mining Engineering
"""
import streamlit as st
import time
import json
from pathlib import Path
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Mine SLM | Safety Management Plan",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Mining Engineering Theme
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1A365D 0%, #2B6CB0 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        color: white !important;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
    }
    .main-header p {
        color: #E2E8F0;
        font-size: 1.05rem;
        margin-top: 6px;
        margin-bottom: 0;
    }
    .sub-badge {
        background-color: rgba(255, 255, 255, 0.2);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin-right: 8px;
        display: inline-block;
    }
    .grounded-card {
        background-color: #F7FAFC;
        border-left: 5px solid #3182CE;
        padding: 18px;
        border-radius: 8px;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .citation-box {
        background-color: #EDF2F7;
        border: 1px solid #CBD5E0;
        border-radius: 6px;
        padding: 12px;
        margin-top: 8px;
        font-size: 0.9rem;
    }
    .statutory-tag {
        background-color: #2B6CB0;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .risk-badge {
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Imports from project modules
from src.config import SUPPORTED_LANGUAGES, PROCESSED_CHUNKS_PATH, DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP
from src.ingestion.data_builder import build_data_repository
from src.ingestion.loader import DocumentLoader
from src.retrieval.hybrid_engine import HybridRetrievalEngine
from src.generation.slm_engine import SLMGenerationEngine
from src.smp_generator.plan_generator import SafetyManagementPlanGenerator
from src.smp_generator.risk_assessment import RiskMatrixManager, calculate_risk_level, LIKELIHOOD_LABELS, CONSEQUENCE_LABELS
from src.smp_generator.checklists import STANDARD_CHECKLISTS
from src.evaluation.benchmark import EvaluationBenchmark

# Cached System Initialization
@st.cache_resource(show_spinner="Initializing Mine SLM Hybrid RAG System...")
def initialize_system():
    # 1. Ensure raw docs and evaluation set are built
    build_data_repository()
    
    # 2. Ingest and chunk documents
    loader = DocumentLoader()
    chunks = loader.load_all_documents()
    
    # 3. Initialize Hybrid Retrieval Engine (BM25 + Dense Vector FAISS + RRF)
    hybrid_engine = HybridRetrievalEngine(chunks)
    
    # 4. Initialize SLM Generation Engine
    slm_engine = SLMGenerationEngine()
    
    # 5. Initialize SMP Generator
    smp_gen = SafetyManagementPlanGenerator()
    
    return loader, chunks, hybrid_engine, slm_engine, smp_gen

loader, chunks, hybrid_engine, slm_engine, smp_gen = initialize_system()

# Sidebar: System Metadata & Controls
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/8/87/National_Institute_of_Technology_Karnataka_Logo.svg/220px-National_Institute_of_Technology_Karnataka_Logo.svg.png", width=70)
    st.markdown("### **NITK Surathkal**")
    st.caption("Department of Mining Engineering")
    st.markdown("---")
    
    st.markdown("#### ⚙️ **Language & Query Settings**")
    selected_lang = st.selectbox(
        "Interface & Response Language:",
        options=list(SUPPORTED_LANGUAGES.keys()),
        format_func=lambda x: SUPPORTED_LANGUAGES[x],
        index=0
    )
    
    st.markdown("#### 🔍 **Hybrid RAG Configuration**")
    retrieval_k = st.slider("Top Passages (k):", min_value=1, max_value=8, value=3)
    
    doc_filter_options = ["ALL", "DGMS-CMR-2017", "DGMS-CIRCULAR-2020-02", "DGMS-CIRCULAR-2021-06", "MINES-ACT-1952", "MINE-PLAN-GEVRA-OPENCAST", "MINE-PLAN-MOONIDIH-UNDERGROUND"]
    selected_doc_filter = st.selectbox("Regulatory Scope Filter:", options=doc_filter_options, index=0)
    
    st.markdown("---")
    st.markdown("#### 📊 **Knowledge Base Status**")
    st.info(f"**Indexed Passages:** `{len(chunks)} Chunks`\n\n**Lexical:** BM25Okapi ($k_1=1.5, b=0.75$)\n\n**Dense Vector:** FAISS FlatIP (Cosine Sim)\n\n**Fusion:** RRF ($k=60$)")
    
    st.markdown("---")
    st.caption("Mine SLM Project | NITK Surathkal © 2026")

# Header Banner
st.markdown("""
<div class="main-header">
    <h1>⛏️ MINE SLM FOR SAFETY MANAGEMENT PLAN</h1>
    <p>AI-Based Platform Built on Hybrid RAG for Grounded, Multilingual Mine-Safety Information Access for Indian Mines</p>
    <div style="margin-top: 12px;">
        <span class="sub-badge">🏛️ NITK Surathkal</span>
        <span class="sub-badge">📜 DGMS CMR 2017 & MMR 1961</span>
        <span class="sub-badge">🔀 Hybrid RAG (BM25 + FAISS + RRF)</span>
        <span class="sub-badge">🌐 Multilingual AI</span>
        <span class="sub-badge">🛡️ ISO 31000 HIRA</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tab_chat, tab_smp, tab_risk, tab_checklists, tab_kb, tab_eval = st.tabs([
    "💬 Multilingual Safety Query",
    "📋 SMP Generator (Appendix C)",
    "⚠️ Risk Matrix & Hazards (ISO 31000)",
    "✅ Operational Safety Checklists",
    "📚 Regulatory Knowledge Base",
    "📈 Evaluation & Benchmark (P@k, MRR)"
])

# ==========================================
# TAB 1: Multilingual Safety Query & RAG
# ==========================================
with tab_chat:
    st.markdown("### 💬 Grounded Mine Safety Information Retrieval")
    st.caption("Ask queries regarding DGMS regulations, haul road specifications, bench dimensions, blasting clearance, ventilation standards, or mine-specific parameters.")

    col_q1, col_q2 = st.columns([3, 1])
    with col_q1:
        # Sample prompt selector
        sample_queries = [
            "What are the statutory requirements for the Safety Management Plan under Regulation 104 of Coal Mines Regulations 2017?",
            "What is the maximum permissible gradient and minimum berm height for opencast haul roads?",
            "ओपनकास्ट खदान में ब्लास्टिंग के समय डेंजर जोन की दूरी कितनी होनी चाहिए और क्या सावधानियां आवश्यक हैं? (Hindi)",
            "भूमिगत कोयला खदान में मीथेन (Inflammable gas) की अधिकतम अनुमेय सीमा क्या है? (Hindi)",
            "What are the bench dimensions and haul road parameters at Gevra Opencast Project?",
            "What specific slope stability monitoring is mandated for deep opencast pits exceeding 100 metres depth?",
            "What are the quantum computing requirements for longwall face shearers according to DGMS? (Test Abstention)"
        ]
        chosen_sample = st.selectbox("💡 Quick Sample Queries:", ["-- Select or Type Custom Query --"] + sample_queries)
        
        default_val = chosen_sample if chosen_sample != "-- Select or Type Custom Query --" else ""
        user_query = st.text_input("Enter your mine safety question:", value=default_val, placeholder="e.g. What is the minimum berm height on opencast haul roads?")

    with col_q2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        execute_btn = st.button("🔍 Search & Generate", type="primary", use_container_width=True)

    if execute_btn and user_query.strip():
        with st.spinner("Executing Hybrid Retrieval (BM25 + FAISS Dense Vector + RRF) and Grounded SLM Generation..."):
            t_start = time.time()
            
            # Hybrid Retrieval
            retrieved_chunks = hybrid_engine.search(
                user_query,
                top_k=retrieval_k,
                filter_doc_id=selected_doc_filter if selected_doc_filter != "ALL" else None
            )
            
            # Generation
            res = slm_engine.generate_response(user_query, retrieved_chunks, target_lang=selected_lang)
            latency = time.time() - t_start

        # Display Response
        st.markdown("---")
        res_col1, res_col2 = st.columns([3, 1])
        with res_col1:
            if res["abstained"]:
                st.error("⚠️ **System Grounded Abstention Triggered**")
            else:
                st.success("✅ **Grounded Statutory Response**")
        with res_col2:
            st.metric("Groundedness Confidence", f"{int(res['confidence_score'] * 100)}%", delta=f"{latency:.2f}s latency")

        st.markdown(res["answer"])
        st.caption(f"🤖 **Model Engine:** `{res['model_used']}`")

        # Traceability & Citations Accordion
        if res["citations"]:
            with st.expander(f"📑 Authoritative Source References & Citations ({len(res['citations'])} sources)"):
                for cit in res["citations"]:
                    st.markdown(f"""
                    <div class="citation-box">
                        <span class="statutory-tag">[{cit['citation_number']}] {cit['document_id']}</span>
                        <strong>{cit['document_title']}</strong> — <em>{cit['section_clause']} (Page {cit['page_number']})</em><br/>
                        <span style="font-size:0.8rem; color:#4A5568;">Issuing Authority: {cit['issuing_authority']} | Status: {cit['revision_status']} | Retrieval: {cit['retrieval_method']}</span>
                        <p style="margin-top:6px; font-style:italic; color:#2D3748;">"{cit['snippet']}"</p>
                    </div>
                    """, unsafe_allow_html=True)

        # Retrieval Evidence Inspector
        with st.expander("🔬 Hybrid RAG Passage Inspector (BM25 vs Dense Vector vs RRF)"):
            ev_data = []
            for c in retrieved_chunks:
                ev_data.append({
                    "RRF Rank": c.get("rrf_rank"),
                    "RRF Score": c.get("rrf_score"),
                    "Doc ID": c.get("doc_id"),
                    "Section / Clause": c.get("section_clause"),
                    "Page": c.get("page_number"),
                    "BM25 Rank (Score)": f"#{c.get('bm25_rank')} ({c.get('bm25_score')})",
                    "Vector Rank (Score)": f"#{c.get('vector_rank')} ({c.get('vector_score')})",
                    "Method": c.get("retrieval_method")
                })
            st.dataframe(pd.DataFrame(ev_data), use_container_width=True)

# ==========================================
# TAB 2: Safety Management Plan (Appendix C)
# ==========================================
with tab_smp:
    st.markdown("### 📋 Automated Statutory Safety Management Plan (SMP) Generator")
    st.caption("Formulates a comprehensive 10-section Safety Management Plan conforming strictly to CMR 2017 Regulation 104, DGMS Circular 02/2020, and Appendix C.")

    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        mine_name_in = st.text_input("Mine Name:", value="Gevra Mega Opencast Project")
        company_in = st.text_input("Operating Company:", value="South Eastern Coalfields Limited (SECL)")
        mine_type_in = st.selectbox("Mine Working Type:", ["Opencast Coal Mine", "Underground Coal Mine (Longwall)", "Metalliferous Open Pit", "Underground Metal Mine"])
    with col_s2:
        capacity_in = st.text_input("Annual Capacity:", value="50.0 MTPA")
        depth_in = st.text_input("Current Pit / Working Depth:", value="120 metres")
        workforce_in = st.text_input("Total Workforce on Rolls:", value="2,450 personnel")
    with col_s3:
        manager_in = st.text_input("Certified Mine Manager:", value="Sri R. K. Sharma (First Class Mgr)")
        safety_officer_in = st.text_input("Designated Safety Officer:", value="Er. A. K. Verma (Chief Safety Officer)")
        bench_ht_in = st.text_input("Bench Height / Seam Details:", value="15.0m OB / 12.0m Coal")

    gen_smp_btn = st.button("📄 Generate Statutory SMP Document", type="primary")

    if gen_smp_btn or "generated_smp" in st.session_state:
        if gen_smp_btn:
            mine_params = {
                "mine_name": mine_name_in,
                "company": company_in,
                "mine_type": mine_type_in,
                "capacity": capacity_in,
                "pit_depth": depth_in,
                "workforce": workforce_in,
                "manager_name": manager_in,
                "safety_officer": safety_officer_in
            }
            # Retrieve relevant statutory clauses from hybrid knowledge base
            stat_chunks = hybrid_engine.search("Safety Management Plan Regulation 104 Hazard Identification Risk Assessment HIRA", top_k=4)
            st.session_state["generated_smp"] = smp_gen.generate_plan(mine_params, stat_chunks)

        smp = st.session_state["generated_smp"]
        st.success(f"Generated: {smp['title']}")
        
        # Action buttons
        d_col1, d_col2 = st.columns([1, 4])
        with d_col1:
            st.download_button(
                label="📥 Download Plan (Markdown)",
                data=smp["markdown"],
                file_name=f"Safety_Management_Plan_{mine_name_in.replace(' ', '_')}.md",
                mime="text/markdown"
            )

        st.markdown("---")
        
        # Structured Tabbed Section Viewer
        s_tabs = st.tabs([
            "1. Mine Overview", "2. Scope & Goals", "3. Regulations", "4. Risk Matrix (HIRA)",
            "5. Controls", "6. Responsibilities", "7. Emergency & TARP", "8. Monitoring", "9. Traceability", "10. Review & Signatures"
        ])
        
        sec_keys = list(smp["sections"].keys())
        for idx, stab in enumerate(s_tabs):
            with stab:
                st.markdown(smp["sections"][sec_keys[idx]], unsafe_allow_html=True)

# ==========================================
# TAB 3: Risk Matrix & Principal Hazards (ISO 31000)
# ==========================================
with tab_risk:
    st.markdown("### ⚠️ Hazard Identification and 5x5 Risk Matrix (HIRA)")
    st.caption("Standardized under ISO 31000:2009 and DGMS (Tech) Circular No. 02 of 2020: Risk Score = Likelihood (1-5) x Consequence (1-5).")

    risk_mgr = RiskMatrixManager()

    # Visual 5x5 Heatmap
    st.markdown("#### 🧮 5x5 Risk Matrix Grid")
    matrix_cols = st.columns(6)
    matrix_cols[0].markdown("**Likelihood \\ Consequence**")
    for c in range(1, 6):
        matrix_cols[c].markdown(f"**C{c}**")

    for l in range(5, 0, -1):
        m_row = st.columns(6)
        m_row[0].markdown(f"**L{l}**")
        for c in range(1, 6):
            score = l * c
            info = calculate_risk_level(score)
            # Find if any active hazards have this score
            matching_haz = [h["id"] for h in risk_mgr.hazards if h["likelihood"] == l and h["consequence"] == c]
            haz_tag = f"<br/><span style='font-size:0.75rem;font-weight:normal;'>{', '.join(matching_haz)}</span>" if matching_haz else ""
            m_row[c].markdown(
                f"<div style='background-color:{info['color']}; color:white; text-align:center; padding:10px; border-radius:6px; font-weight:bold; margin-bottom:4px;'>"
                f"{score}{haz_tag}</div>",
                unsafe_allow_html=True
            )

    st.markdown("---")
    st.markdown("#### 📋 Principal Mining Hazards (PMH) Register")
    
    h_data = []
    for h in risk_mgr.hazards:
        h_data.append({
            "Hazard ID": h["id"],
            "Category": h["category"],
            "Hazard Description": h["description"],
            "L (1-5)": h["likelihood"],
            "C (1-5)": h["consequence"],
            "Risk Score": h["risk_score"],
            "Risk Level": h["risk_level"],
            "Applicable Regulation": h["regulation"],
            "Primary Controls": "; ".join(h["controls"])
        })
    st.dataframe(pd.DataFrame(h_data), use_container_width=True)

    # Add custom hazard form
    with st.expander("➕ Add Custom Mine-Specific Hazard"):
        with st.form("custom_hazard_form"):
            c_cat = st.selectbox("Category:", ["Ground Instability", "Haul Road", "Explosives/Blasting", "Inundation", "Mine Gases", "Mechanical/Electrical", "Health & Hygiene"])
            c_desc = st.text_input("Hazard Description:", placeholder="e.g. Unstable dump crest near haul road junction")
            c_l = st.slider("Likelihood (1=Rare to 5=Almost Certain):", 1, 5, 3)
            c_c = st.slider("Consequence (1=Insignificant to 5=Catastrophic):", 1, 5, 4)
            c_ctrl = st.text_area("Control Measures (one per line):", "Erect catch berm >= 2.7m\nInstall geotechnical crack gauges\nRestrict speed to 15 km/h")
            c_reg = st.text_input("Statutory Reference:", "CMR 2017 Regulation 106")
            submit_h = st.form_submit_button("Record Hazard to Register")
            if submit_h:
                new_h = risk_mgr.add_custom_hazard(c_cat, c_desc, c_l, c_c, c_ctrl.split("\n"), c_reg)
                st.success(f"Recorded {new_h['id']} with Risk Score {new_h['risk_score']} ({new_h['risk_level']})!")
                st.rerun()

# ==========================================
# TAB 4: Operational Safety Checklists
# ==========================================
with tab_checklists:
    st.markdown("### ✅ Operational Safety Checklists & Shift Audit Forms")
    st.caption("Actionable digital checklists for statutory mine personnel (Mine Manager, Safety Officer, Overman, Mining Sirdar).")

    chk_choice = st.selectbox(
        "Select Checklist Type:",
        options=list(STANDARD_CHECKLISTS.keys()),
        format_func=lambda k: STANDARD_CHECKLISTS[k]["title"]
    )
    
    active_chk = STANDARD_CHECKLISTS[chk_choice]
    st.markdown(f"**Target Role:** `{active_chk['role']}` | **Statutory Authority:** `{active_chk['statutory_ref']}`")
    
    st.markdown("---")
    responses = {}
    for item in active_chk["items"]:
        col_c1, col_c2 = st.columns([3, 1])
        with col_c1:
            st.markdown(f"**{item['id']}**: {item['question']}")
            st.caption(f"Statutory Benchmark: {item['standard']}")
        with col_c2:
            responses[item["id"]] = st.radio(f"Status ({item['id']}):", ["Compliant (Pass)", "Non-Compliant (Fail)", "Action Required"], horizontal=True, label_visibility="collapsed")
        st.markdown("<hr style='margin: 8px 0;'>", unsafe_allow_html=True)

    if st.button("📋 Submit Audit Inspection Record"):
        fails = [k for k, v in responses.items() if v == "Non-Compliant (Fail)"]
        warns = [k for k, v in responses.items() if v == "Action Required"]
        if fails:
            st.error(f"🚨 **Statutory Non-Compliance Detected!** {len(fails)} items failed inspection ({', '.join(fails)}). Immediate remedial action required under CMR 2017.")
        elif warns:
            st.warning(f"⚠️ **Attention Required:** {len(warns)} items require corrective action ({', '.join(warns)}).")
        else:
            st.success("✅ **Inspection Passed 100%:** All statutory standards met. Shift authorized to proceed.")

# ==========================================
# TAB 5: Regulatory Knowledge Base & Chunker
# ==========================================
with tab_kb:
    st.markdown("### 📚 Regulatory Knowledge Base & Document Chunking Explorer")
    st.caption("Inspect indexed passages, Table A.1 metadata structures, and test the sliding window chunking algorithm (S = C - O).")

    # Document Chunking Formula Display
    st.info(r"**Governing Chunking Formula (Section 3.5.1):** $S = C - O$, where $C$ is token size, $O$ is overlap, and $S$ is step size.")

    # Upload custom document
    with st.expander("📤 Ingest New Regulatory Circular or Mine Plan (PDF or Text)"):
        uploaded_file = st.file_uploader("Upload DGMS Document or Mine Plan:", type=["pdf", "txt", "md"])
        if uploaded_file is not None:
            up_doc_id = st.text_input("Assign Document ID:", value=f"DOC-{uploaded_file.name[:12].upper()}")
            up_title = st.text_input("Document Title:", value=uploaded_file.name.replace("_", " "))
            up_auth = st.text_input("Issuing Authority:", value="Directorate General of Mines Safety (DGMS)")
            if st.button("🚀 Process & Ingest Document"):
                bytes_data = uploaded_file.read()
                new_chk = loader.process_custom_upload(
                    bytes_data,
                    uploaded_file.name,
                    {
                        "doc_id": up_doc_id,
                        "doc_title": up_title,
                        "issuing_authority": up_auth,
                        "publication_date": "2026",
                        "revision_status": "Uploaded Document"
                    }
                )
                st.success(f"Successfully processed and indexed {len(new_chk)} new passages!")
                st.cache_resource.clear()
                st.rerun()

    # Knowledge Base Chunks Table
    st.markdown("#### 📑 Indexed Document Chunks (Table A.1 Metadata Schema)")
    df_chunks = pd.DataFrame([{
        "Chunk ID": c["chunk_id"],
        "Doc ID": c["doc_id"],
        "Document Title": c["doc_title"],
        "Section / Clause": c["section_clause"],
        "Page": c["page_number"],
        "Tokens": c["token_count"],
        "Issuing Authority": c["issuing_authority"],
        "Status": c["revision_status"]
    } for c in chunks])
    
    st.dataframe(df_chunks, use_container_width=True)

# ==========================================
# TAB 6: Evaluation & Benchmarking Suite
# ==========================================
with tab_eval:
    st.markdown("### 📈 Evaluation & Benchmarking Suite (Section 3.5.6 & Appendix B)")
    st.caption("Quantitative performance evaluation against standard test queries across Precision@k, Recall@k, Mean Reciprocal Rank (MRR), and Groundedness.")

    bench_k = st.slider("Benchmark Top-k evaluation parameter:", min_value=1, max_value=5, value=3)
    
    run_eval_btn = st.button("⚡ Run Full Automated Benchmark", type="primary")

    if run_eval_btn or "eval_results" in st.session_state:
        if run_eval_btn:
            with st.spinner("Executing evaluation queries, calculating Precision@k, Recall@k, MRR, and Groundedness..."):
                evaluator = EvaluationBenchmark(hybrid_engine, slm_engine)
                st.session_state["eval_results"] = evaluator.run_benchmark(k=bench_k)

        eval_res = st.session_state["eval_results"]
        
        # Display Top Metrics
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Mean Reciprocal Rank (MRR)", f"{eval_res['mean_reciprocal_rank_MRR']:.3f}", "Rank Fidelity")
        m2.metric(f"Precision@{bench_k}", f"{eval_res['precision_at_k'] * 100:.1f}%", "Retrieved Relevance")
        m3.metric(f"Recall@{bench_k}", f"{eval_res['recall_at_k'] * 100:.1f}%", "Retrieval Coverage")
        m4.metric("Avg Groundedness", f"{eval_res['average_groundedness_score'] * 100:.1f}%", "Zero Hallucination")
        m5.metric("Avg Latency", f"{eval_res['average_latency_seconds']:.2f} s", "Hybrid Speed")

        st.markdown("---")
        st.markdown("#### 🧪 Detailed Test Set Query Evaluations (Appendix B Table B.1)")
        df_eval = pd.DataFrame(eval_res["detailed_query_evaluations"])
        st.dataframe(df_eval[[
            "query_id", "language", "query_text", "expected_source", "retrieved_top_doc",
            "precision_at_k", "recall_at_k", "reciprocal_rank", "grounded_score", "abstained", "latency_sec"
        ]], use_container_width=True)
