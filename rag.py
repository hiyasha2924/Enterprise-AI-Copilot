# rag.py

from index import create_faiss_index
from query_engine import get_answer

def main():
    print("📄 Loading all PDFs from /docs...")
    create_faiss_index()

    print("\n✅ PDFs indexed. Ask anything!\n")
    while True:
        question = input("🧠 You: ")
        if question.lower() in ["exit", "quit"]:
            break
        answer = get_answer(question)
        print(f"🤖 Assistant: {answer}\n")

if __name__ == "__main__":
    main()
