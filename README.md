# Mine SLM for Safety Management Plan
**AI-Based Platform Built on Hybrid RAG for Grounded, Multilingual Mine-Safety Information Access for Indian Mines**

> **Major Project Report Implementation**  
> **Institution:** National Institute of Technology Karnataka (NITK), Surathkal  
> **Department:** Department of Mining Engineering  
> **Academic Year:** 2026–2027  
> **Supervisor:** Dr. Akhil Avchar (Assistant Professor)  
> **HOD:** Dr. Harsha Vardhan (Professor)  
> **Authors:** Aayush Dubey (231MN001), Aditya Kumar Sahu (231MN003), Raut Akash Naresh (231MN038)

---

## 🏗️ System Architecture & Workflow

The platform implements the complete 4-layer architecture detailed in Chapter 3:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        1. User Interface Layer                         │
│  - Multilingual Query Interface (EN, HI, BN, OR, TE, KN, MR)           │
│  - Safety Management Plan (SMP) Generator (Appendix C)                 │
│  - 5x5 Risk Matrix & Hazard Register (ISO 31000 & DGMS Circular 02/20) │
│  - Operational Safety Checklists (Bench, Haul Road, Blasting, Gas)     │
│  - Grounded Evidence & Citation Drawer (Table A.1 Metadata)            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│                    2. Hybrid Retrieval Layer (RAG)                     │
│  ┌─────────────────────────────┐     ┌──────────────────────────────┐  │
│  │   Lexical Search (BM25)     │     │ Dense Vector Search (FAISS)  │  │
│  │  - BM25Okapi Equation 3.5.3 │     │ - Cosine Sim Equation 3.5.2  │  │
│  │  - Mining tokenization      │     │ - Sublinear TF-IDF + Char N  │  │
│  └──────────────┬──────────────┘     └──────────────┬───────────────┘  │
│                 │                                   │                  │
│                 └──────────────► ◄──────────────────┘                  │
│                                  │                                     │
│                 Reciprocal Rank Fusion (RRF, k=60)                     │
│                       RRF(d) = Σ 1 / (k + rank_r(d))                   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Top-k Grounded Chunks
┌───────────────────────────────────▼────────────────────────────────────┐
│                   3. SLM Generation & Grounding Layer                  │
│  - Compact SLM Architecture: Gemma 3 4B IT Prompt Directives           │
│  - Grounding Verification & Abstention Engine (Anti-Hallucination)    │
│  - Statutory Citation Formatter ([Doc ID, Section, Page])              │
│  - Multilingual Translation & Cultural Preservations                   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│                  4. Knowledge Base & Document Store                    │
│  - The Coal Mines Regulations, 2017 (CMR 2017: Reg 104, 106, 83, 171)  │
│  - DGMS Technical Circulars (02/2020 HIRA, 06/2021 SSR Slope radar)    │
│  - The Mines Act, 1952 (Sections 18, 23)                               │
│  - Mine Plans (Gevra Mega Opencast SECL, Moonidih Underground BCCL)   │
│  - Dynamic PDF Ingestion via PyMuPDF (fitz)                            │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📐 Mathematical Governing Principles Implemented

### 1. Document Chunking & Step Size (Section 3.5.1)
$$S = C - O$$
- $C = 350$ tokens (chunk size)
- $O = 75$ tokens (overlap)
- $S = 275$ tokens (step size between adjacent chunks)

### 2. Text Embeddings and Vector Cosine Similarity (Section 3.5.2)
$$\text{sim}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$$
- Indexed using `FAISS FlatIP` on unit-normalized vectors.

### 3. BM25 Lexical Ranking (Section 3.5.3)
$$\text{BM25}(D, Q) = \sum_{q_i \in Q} \text{IDF}(q_i) \frac{f(q_i, D)(k_1 + 1)}{f(q_i, D) + k_1 \left(1 - b + b \frac{|D|}{\text{avgdl}}\right)}$$
- Hyperparameters: $k_1 = 1.5, b = 0.75$.

### 4. Reciprocal Rank Fusion (Section 3.5.4)
$$\text{RRF}(d) = \sum_{r \in R} \frac{1}{k + \text{rank}_r(d)}$$
- Constant $k = 60$. Combines BM25 and Vector candidate rankings.

### 5. Evaluation Metrics (Section 3.5.6)
- **Precision@k:** $P@k = \frac{\text{Relevant passages in top } k}{k}$
- **Recall@k:** $R@k = \frac{\text{Relevant passages in top } k}{\text{Total relevant passages}}$
- **Mean Reciprocal Rank (MRR):** $\text{MRR} = \frac{1}{N} \sum_{i=1}^N \frac{1}{r_i}$

---

## 🚀 Quickstart Guide

### 1. Installation
Ensure Python 3.11+ is installed, then run:
```bash
pip install -r requirements.txt
```

### 2. Running Automated Unit & Integration Tests
```bash
python tests/test_hybrid_rag.py
```
*Validates data repository creation, PyMuPDF PDF generation, BM25, FAISS, RRF fusion, grounded abstention, SMP generation, and benchmark evaluation.*

### 3. Launching the Web Frontend
```bash
python run_server.py
```
Or directly with Streamlit:
```bash
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser.

---

## 📑 Features & Capabilities

1. **Multilingual Regulatory Chat**:
   - Query in **English, हिन्दी (Hindi), বাংলা (Bengali), ଓଡ଼ିଆ (Odia), తెలుగు (Telugu), ಕನ್ನಡ (Kannada), and मराठी (Marathi)**.
   - Grounded citations linking directly to Regulation number, document title, and page.
   - **Abstention Safeguard**: Refuses to hallucinate on out-of-scope or unsupported queries.

2. **Automated Safety Management Plan (SMP) Generator (Appendix C)**:
   - Formulates the full 10-section statutory document under **CMR 2017 Regulation 104**.
   - Incorporates mine operational parameters (opencast bench geometry, haul road specs, gassiness degree).
   - Generates downloadable Markdown, HTML, and formatted reports with official statutory review records.

3. **5x5 Risk Matrix & Principal Mining Hazards (HIRA)**:
   - ISO 31000:2009 and DGMS Circular 02/2020 compliance.
   - Interactive visual heatmap classifying Low, Medium, High, and Critical risks.
   - Form to log custom mine hazards and dynamically re-calculate risk scores.

4. **Operational Safety Checklists**:
   - Pre-Shift Opencast Bench Stability Checklist (CMR Reg 106).
   - Haul Road, Dumper & Berm Safety Audit (CMR Reg 83/84).
   - Shotfiring & Blasting Danger Zone Clearance Protocol (CMR Reg 171/186).
   - Underground Ventilation & Gas Monitoring Checklist (CMR Reg 153/155).

5. **Knowledge Base Explorer & Dynamic Ingestion**:
   - Inspect chunks, token lengths, and Table A.1 metadata.
   - Upload new DGMS circulars or mine plan PDFs for instant indexing.

6. **Automated Evaluation Benchmark Suite**:
   - Built-in test query bank conforming to Appendix B Table B.1.
   - Real-time computation of P@k, R@k, MRR, groundedness, and latency.
