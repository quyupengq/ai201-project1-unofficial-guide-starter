import json
import re
from pathlib import Path

RAW_DIR = Path("documents/raw")
OUT_DIR = Path("data")
OUT_FILE = OUT_DIR / "chunks.json"

TARGET_CHARS = 700
OVERLAP_CHARS = 120


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = text.replace("&amp;", "&")
    text = text.replace("&nbsp;", " ")

    # Remove extra spaces but keep paragraph breaks
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def split_into_units(text: str):
    """
    Split text into paragraph/comment-sized units.
    If a paragraph is very long, split it by sentences.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    units = []

    for para in paragraphs:
        if len(para) <= TARGET_CHARS:
            units.append(para)
        else:
            # Split long paragraphs into sentence-ish pieces
            sentences = re.split(r"(?<=[.!?])\s+", para)
            current = ""

            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue

                if len(current) + len(sentence) + 1 <= TARGET_CHARS:
                    current = f"{current} {sentence}".strip()
                else:
                    if current:
                        units.append(current)
                    current = sentence

            if current:
                units.append(current)

    return [u for u in units if len(u) > 30]


def chunk_text(text: str, source_name: str):
    units = split_into_units(text)
    chunks = []
    current = ""

    for unit in units:
        if len(current) + len(unit) + 2 <= TARGET_CHARS:
            current = f"{current}\n\n{unit}".strip()
        else:
            if current:
                chunks.append(current)

            overlap = current[-OVERLAP_CHARS:] if current else ""
            current = f"{overlap}\n\n{unit}".strip()

    if current:
        chunks.append(current)

    output = []

    for i, chunk in enumerate(chunks):
        output.append({
            "id": f"{source_name}_{i}",
            "source": source_name,
            "chunk_index": i,
            "text": chunk
        })

    return output


def main():
    OUT_DIR.mkdir(exist_ok=True)

    all_chunks = []
    txt_files = sorted(RAW_DIR.glob("*.txt"))

    if not txt_files:
        raise FileNotFoundError("No .txt files found in documents/raw")

    for path in txt_files:
        raw_text = path.read_text(encoding="utf-8")
        cleaned = clean_text(raw_text)
        chunks = chunk_text(cleaned, path.name)
        all_chunks.extend(chunks)

    OUT_FILE.write_text(json.dumps(all_chunks, indent=2), encoding="utf-8")

    print(f"Loaded {len(txt_files)} documents")
    print(f"Created {len(all_chunks)} chunks")
    print(f"Saved chunks to {OUT_FILE}")

    print("\n--- Chunk counts by document ---")
    counts = {}
    for chunk in all_chunks:
        counts[chunk["source"]] = counts.get(chunk["source"], 0) + 1

    for source, count in counts.items():
        print(f"{source}: {count} chunks")

    print("\n--- Sample chunks ---")
    for chunk in all_chunks[:5]:
        print(f"\nSource: {chunk['source']}")
        print(f"Chunk index: {chunk['chunk_index']}")
        print(chunk["text"][:700])
        print("-" * 80)


if __name__ == "__main__":
    main()