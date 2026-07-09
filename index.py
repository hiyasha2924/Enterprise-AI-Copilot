# index.py

import os
import faiss
import pickle
import pdfplumber
from sentence_transformers import SentenceTransformer

CHUNK_SIZE = 300
MODEL_NAME = "all-MiniLM-L6-v2"
INDEX_FILE = "vector_index.faiss"
DOCS_FILE = "docs.pkl"
DOCS_FOLDER = "docs"

def load_all_pdf_texts(folder_path):
    all_text = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            print(f"📄 Reading: {pdf_path}")
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        all_text += text + "\n"
    return all_text.strip()

def chunk_text(text, size=CHUNK_SIZE):
    words = text.split()
    return [' '.join(words[i:i+size]) for i in range(0, len(words), size)]

def create_faiss_index():
    model = SentenceTransformer(MODEL_NAME)
    text = load_all_pdf_texts(DOCS_FOLDER)
    chunks = chunk_text(text)

    print(f"✂️ Total Chunks: {len(chunks)}")

    embeddings = model.encode(chunks, show_progress_bar=True)
    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, INDEX_FILE)
    with open(DOCS_FILE, "wb") as f:
        pickle.dump(chunks, f)

    print("✅ FAISS index and docs saved.")

if __name__ == "__main__":
    create_faiss_index()
