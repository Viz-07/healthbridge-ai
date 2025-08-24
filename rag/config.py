import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
DATA_PATH = "data"
CHROMA_PATH = "chroma_db"
CSV_FILE = "Diseases_Symptoms.csv"

# --- Qdrant configs (placeholder values, uncomment for deployment) ---
QDRANT_URL = None
QDRANT_API_KEY = None
# QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
# QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None) or None
