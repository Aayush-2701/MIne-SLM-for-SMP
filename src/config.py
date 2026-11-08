import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DOCS_DIR = DATA_DIR / "raw_documents"
PROCESSED_CHUNKS_PATH = DATA_DIR / "processed_chunks.json"
EVALUATION_DATASET_PATH = DATA_DIR / "evaluation_dataset.json"
GENERATED_PLANS_DIR = BASE_DIR / "generated_plans"

RAW_DOCS_DIR.mkdir(parents=True, exist_ok=True)
GENERATED_PLANS_DIR.mkdir(parents=True, exist_ok=True)

# Chunking Parameters (Design Calculations Section 3.5.1)
DEFAULT_CHUNK_SIZE = 350       # C = tokens/words per chunk
DEFAULT_CHUNK_OVERLAP = 75     # O = overlap tokens
# Step S = C - O = 275

# Retrieval Hyperparameters
BM25_K1 = 1.5                  # BM25 term saturation parameter
BM25_B = 0.75                  # BM25 document length normalization
RRF_K = 60                     # Reciprocal Rank Fusion constant (Equation 3.5.4)
TOP_K_RETRIEVAL = 5            # Default top-k retrieved chunks

# Grounding & Generation Parameters (Section 3.3.4 & 3.5.5)
MIN_GROUNDING_CONFIDENCE = 0.35  # Threshold below which system abstains
SLM_MODEL_NAME = "Gemma 3 4B IT (Compact SLM)"

# Supported Indian Languages (Section 2.2.5)
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "हिन्दी (Hindi)",
    "bn": "বাংলা (Bengali)",
    "or": "ଓଡ଼ିଆ (Odia)",
    "te": "తెలుగు (Telugu)",
    "kn": "ಕನ್ನಡ (Kannada)",
    "mr": "मराठी (Marathi)"
}
