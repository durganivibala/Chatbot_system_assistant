import os
import chromadb
import subprocess
from sentence_transformers import SentenceTransformer, CrossEncoder
from prompts import SYSTEM_PROMPT
import numpy as np
from embedder import get_embedder
from reranker import get_reranker


CHROMA_PATH = "chroma_db"
GUIDE_COLLECTION_one = "path"
GUIDE_COLLECTION_two="path"
embedder = get_embedder()
reranker = get_reranker()
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")


client = chromadb.PersistentClient(path=CHROMA_PATH)
guide_one = client.get_collection(GUIDE_COLLECTION_one)
guide_two= client.get_collection(GUIDE_COLLECTION_two)

#Tell your model to choose document in case of multiple documents
def select_collection(query: str):
    issue_keywords = ["issue","problem","conflicts"]
    q = query.lower()

    if any(word in q for word in issue_keywords):
        return guide_one
    return guide_two


def retrieve_context(query, top_k=3):

    collection, name = select_collection(query)
    print(f"📌 Using collection: {name}")

    query_embedding = embedder.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=25
    )

    if not results["documents"]:
        return ""

    docs = results["documents"][0]
    scores = reranker.predict([(query, d) for d in docs])

    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    top_docs = [d for d, _ in ranked[:top_k]]

    return "\n".join(top_docs)


def call_ollama(prompt: str) -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],

            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=180,
        )
        output = result.stdout.decode("utf-8").strip()
        return output
    except Exception as e:
        return f"⚠️ Error calling Ollama: {e}"

def compress_context(context: str) -> str:
    compress_prompt = f"""
    You are a context compression engine.
    Rewrite the following text so that it stays complete, factual, and usable by an LLM,
    but reduce verbosity, redundant lines, repeated bullet points, and long explanations.

    Keep ALL technical details, ports, commands, parameters, limits, and critical info.

    Text:
    {context}

    Compressed Text:
    """
    summary = call_ollama(compress_prompt)
    return summary.strip()


def generate_response(user_query, chat_history):
    context = retrieve_context(user_query)
    context = compress_context(context)
    if not context:
        return "I can only answer questions related to the PME System Guide."

    prompt = f"""
{SYSTEM_PROMPT}

Context from PME System Guide:
{context}

Chat History:
{chat_history}

User: {user_query}
Assistant:
"""
    print("Prompt length:", len(prompt))

    response = call_ollama(prompt)
    return response.strip()


