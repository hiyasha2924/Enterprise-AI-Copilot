# query_engine.py

import faiss
import pickle
from sentence_transformers import SentenceTransformer
import subprocess

INDEX_FILE = "vector_index.faiss"
DOCS_FILE = "docs.pkl"
MODEL_NAME = "all-MiniLM-L6-v2"

def load_index_and_docs():
    index = faiss.read_index(INDEX_FILE)
    with open(DOCS_FILE, "rb") as f:
        chunks = pickle.load(f)
    return index, chunks

def query_index(query, top_k=4):
    model = SentenceTransformer(MODEL_NAME)
    query_vec = model.encode([query])
    index, chunks = load_index_and_docs()
    D, I = index.search(query_vec, top_k)
    return [chunks[i] for i in I[0]]

def build_prompt(query, contexts):
    context_text = "\n\n".join(f"- {c}" for c in contexts)
    return f"""You are an AI assistant. Use the following document excerpts to answer the question.

Context:
{context_text}

Question: {query}

Answer:"""

def ask_llm(prompt):
    result = subprocess.run(
        ["ollama", "run", "llama3", prompt],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def get_answer(query):
    contexts = query_index(query)
    final_prompt = build_prompt(query, contexts)
    return ask_llm(final_prompt)
