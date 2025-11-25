import os
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
import numpy as np


os.makedirs("chroma_db", exist_ok=True)

# Local paths (make sure these folders exist)
PDF_PATH = "path"
model = SentenceTransformer('BAAI/bge-large-en-v1.5')

reader = PdfReader(PDF_PATH)
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"


def chunk_text(text, chunk_size=2500, overlap=200):

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

chunks = chunk_text(text)
print(f"📄 Split into {len(chunks)} chunks.")

print("🔹 Loading embedding model...")

embeddings = model.encode(chunks, show_progress_bar=True, convert_to_numpy=True)


client = chromadb.PersistentClient(path="chroma_db")
collection_name = "name of the document"

try:
    collection = client.get_collection(collection_name)
    existing_ids = collection.get()["ids"]
    if existing_ids:
        print(f"🧹 Clearing {len(existing_ids)} existing entries...")
        collection.delete(ids=existing_ids)
except Exception:
    collection = client.create_collection(collection_name)

print("💾 Adding new embeddings...")
for i, chunk in enumerate(chunks):
    collection.add(
        ids=[str(i)],
        embeddings=[embeddings[i].tolist()],
        documents=[chunk],
    )

print(f"✅ Embedded {len(chunks)} chunks successfully into ChromaDB.")
