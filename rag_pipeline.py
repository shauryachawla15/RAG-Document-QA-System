import chromadb
from sentence_transformers import SentenceTransformer
import os


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Persistent Chroma DB (so it doesn’t recreate every run)
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="innovationm_docs")


def load_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


# BETTER CHUNKING
def chunk_text(text):
    # Remove LINKS section completely
    if "LINKS:" in text:
        text = text.split("LINKS:")[0]

    # Split by newline
    raw_chunks = text.split("\n")

    # Clean empty / small lines
    chunks = []
    for chunk in raw_chunks:
        cleaned = chunk.strip()
        if len(cleaned) > 40:   # ignore tiny useless lines
            chunks.append(cleaned)

    return chunks


def store_embeddings(chunks):

    #  Get all existing IDs first
    existing = collection.get()

    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    embeddings = model.encode(chunks)

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"id_{i}" for i in range(len(chunks))]
    )

    print("Embeddings stored properly!")

def query_rag(question):
    query_embedding = model.encode([question])

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=2   # only top 2
    )

    return results["documents"][0]


def main():
    text = load_data("innovationm_data.txt")
    chunks = chunk_text(text)

    print(f"Total chunks created: {len(chunks)}")

    store_embeddings(chunks)

    print("\nAsk a question about the website:")
    question = input(">> ")

    results = query_rag(question)

    print("\nTop Relevant Chunks:\n")
    for doc in results:
        print(doc)
        print("-" * 50)


if __name__ == "__main__":
    main()