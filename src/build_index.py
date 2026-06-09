import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = Path("data/chunks.json")
CHROMA_DIR = "data/chroma_db"
COLLECTION_NAME = "internship_difficulty"


def main():
    if not CHUNKS_FILE.exists():
        raise FileNotFoundError("data/chunks.json not found. Run python src/ingest.py first.")

    chunks = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))

    if not chunks:
        raise ValueError("No chunks found in data/chunks.json")

    print(f"Loaded {len(chunks)} chunks")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    texts = [chunk["text"] for chunk in chunks]
    ids = [chunk["id"] for chunk in chunks]
    metadatas = [
        {
            "source": chunk["source"],
            "chunk_index": chunk["chunk_index"],
        }
        for chunk in chunks
    ]

    print("Creating embeddings...")
    embeddings = model.encode(texts).tolist()

    client = chromadb.PersistentClient(path=CHROMA_DIR)

    # Rebuild collection from scratch each time
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(name=COLLECTION_NAME)

    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    print(f"Saved {len(chunks)} chunks to ChromaDB collection: {COLLECTION_NAME}")
    print(f"Database location: {CHROMA_DIR}")


if __name__ == "__main__":
    main()