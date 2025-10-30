import chromadb
from sentence_transformers import SentenceTransformer
from prompts import SYSTEM_PROMPT
import subprocess
import json

# -----------------------------
# ⚙️ Configuration
# -----------------------------
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
OLLAMA_MODEL = "llama3"  # You can replace with 'llama3', 'phi3', etc.

# -----------------------------
# 🔧 Initialize models and DB
# -----------------------------
embedder = SentenceTransformer(EMBED_MODEL)
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("pme_guide")


# -----------------------------
# 🧩 Helper functions
# -----------------------------
def retrieve_context(query, top_k=3):
    """Retrieve most relevant chunks from ChromaDB."""
    query_embedding = embedder.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    if not results["documents"]:
        return ""
    return "\n".join(results["documents"][0])


def call_ollama(prompt: str) -> str:
    """Send the prompt to local Ollama model and return the response."""
    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120,
        )
        output = result.stdout.decode("utf-8").strip()
        return output
    except Exception as e:
        return f"⚠️ Error calling Ollama: {e}"


def generate_response(user_query, chat_history):
    """RAG + custom prompt integration with Ollama."""
    context = retrieve_context(user_query)

    if not context:
        return "I can only answer questions related to the PME System Guide."

    # Construct the final prompt for the LLM
    full_prompt = f"""
{SYSTEM_PROMPT}

Context from PME System Guide:
{context}

Chat History:
{chat_history}

User: {user_query}
Assistant:
"""
    response = call_ollama(full_prompt)
    return response.strip()
