import os
from dotenv import load_dotenv
from groq import Groq

from src.retrieve import retrieve

load_dotenv()

MODEL_NAME = "llama-3.3-70b-versatile"


def build_context(retrieved_chunks):
    context_parts = []

    for i, chunk in enumerate(retrieved_chunks, start=1):
        source = chunk["source"]
        chunk_index = chunk["chunk_index"]
        text = chunk["text"]

        context_parts.append(
            f"[Chunk {i} | Source: {source} | Chunk index: {chunk_index}]\n{text}"
        )

    return "\n\n---\n\n".join(context_parts)


def ask(question: str):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("Missing GROQ_API_KEY. Add it to your .env file.")

    retrieved_chunks = retrieve(question, top_k=5)
    context = build_context(retrieved_chunks)

    sources = []
    for chunk in retrieved_chunks:
        if chunk["source"] not in sources:
            sources.append(chunk["source"])

    system_prompt = """
You are a grounded RAG assistant for a student internship difficulty guide.

Rules:
1. Answer using ONLY the provided context chunks.
2. Do not use outside knowledge.
3. If the context does not directly answer the question, say:
   "I don't have enough information from the documents to answer that."
4. Be honest about uncertainty.
5. Mention the source document names that support the answer.
6. Do not invent statistics, companies, numbers, or claims that are not in the context.
"""

    user_prompt = f"""
Question:
{question}

Context chunks:
{context}

Write a helpful answer grounded only in the context.
"""

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()},
        ],
        temperature=0.2,
        max_tokens=700,
    )

    answer = response.choices[0].message.content.strip()

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": retrieved_chunks,
    }


def main():
    test_questions = [
        "Why do students say internships are hard to get?",
        "Do students report being ghosted after applying to internships?",
        "Does having good grades guarantee an internship?",
        "What advice do students give for improving internship chances?",
        "What exact company hires the most students?",
    ]

    for question in test_questions:
        print("\n" + "=" * 100)
        print(f"QUESTION: {question}")
        print("=" * 100)

        result = ask(question)

        print("\nANSWER:")
        print(result["answer"])

        print("\nSOURCES:")
        for source in result["sources"]:
            print(f"- {source}")

        print("\nRETRIEVED CHUNKS:")
        for chunk in result["retrieved_chunks"]:
            print(
                f"- {chunk['source']} | chunk {chunk['chunk_index']} | distance {chunk['distance']}"
            )


if __name__ == "__main__":
    main()