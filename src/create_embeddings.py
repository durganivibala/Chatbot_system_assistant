import os
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb

# --- Ensure persistent directory ---
os.makedirs("chroma_db", exist_ok=True)

# --- Load PDF content ---
pdf_path = r"E:\Chatbot_PME\guide\PME System Guide 2024.pdf"
reader = PdfReader(pdf_path)

text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

# --- Split into chunks ---
def chunk_text(text, chunk_size=800, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

chunks = chunk_text(text)

# --- Initialize sentence-transformer embeddings ---
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embeddings = embedder.encode(chunks, show_progress_bar=True)

# --- Initialize ChromaDB persistent client ---
client = chromadb.PersistentClient(path= "chroma_db")
collection_name = "pme_guide"

# --- If collection exists, clear it safely ---
try:
    collection = client.get_collection(collection_name)
    all_ids = collection.get()["ids"]
    if all_ids:
        print(f"🧹 Clearing {len(all_ids)} existing records from '{collection_name}'...")
        collection.delete(ids=all_ids)
except Exception:
    # If collection doesn’t exist, create it fresh
    collection = client.create_collection(collection_name)

# --- Add new embeddings ---
print(f"💾 Adding {len(chunks)} new chunks...")
for i, chunk in enumerate(chunks):
    collection.add(
        ids=[str(i)],
        embeddings=[embeddings[i].tolist()],
        documents=[chunk]
    )

print(f"✅ Successfully embedded {len(chunks)} chunks into ChromaDB.")
