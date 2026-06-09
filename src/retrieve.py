import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DIR = "data/chroma_db"
COLLECTION_NAME = "internship_difficulty"
TOP_K = 5


def retrieve(query: str, top_k: int = TOP_K):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = model.encode([query]).tolist()[0]

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    retrieved = []

    for doc, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        retrieved.append({
            "text": doc,
            "source": metadata["source"],
            "chunk_index": metadata["chunk_index"],
            "distance": distance,
        })

    return retrieved


def main():
    test_queries = [
        "Why do students say internships are hard to get?",
        "Do students report being ghosted after applying to internships?",
        "Does having good grades guarantee an internship?",
        "What advice do students give for improving internship chances?",
        "Are students worried that not getting an internship will hurt them after graduation?",
    ]

    for query in test_queries:
        print("\n" + "=" * 100)
        print(f"QUERY: {query}")
        print("=" * 100)

        results = retrieve(query)

        for i, result in enumerate(results, start=1):
            print(f"\nResult {i}")
            print(f"Source: {result['source']}")
            print(f"Chunk index: {result['chunk_index']}")
            print(f"Distance: {result['distance']}")
            print("Text:")
            print(result["text"][:1000])
            print("-" * 100)


if __name__ == "__main__":
    main()