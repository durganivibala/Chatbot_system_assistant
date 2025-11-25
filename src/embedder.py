import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HUB_DISABLE_SSL_VERIFY"] = "1"
from sentence_transformers import SentenceTransformer

# Load ONCE & reuse everywhere
_embedder = SentenceTransformer("BAAI/bge-large-en-v1.5")

def get_embedder():
    return _embedder
