from app.rag.chunking import load_policies, create_chunks
from app.rag.embeddings import create_embedding
from app.rag.vector_store import store_chunks
from app.rag.vector_store import get_collection


# Load policy data
policies = load_policies("data/policies.json")

print("Total policies:", len(policies))
print("First policy:", policies[0]["policy_name"])


chunks = create_chunks(policies)

# Create an embedding for every chunk
for chunk in chunks:

    text = chunk["text"]

    embedding = create_embedding(text)

    chunk["embedding"] = embedding


# Debug check
for i, chunk in enumerate(chunks):
    print(i, chunk["chunk_id"], "embedding" in chunk)


# Store only after every chunk has an embedding
store_chunks(chunks)

collection = get_collection()

print("Chunks stored in ChromaDB:", collection.count())