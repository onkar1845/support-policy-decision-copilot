import chromadb


def get_collection():

    # Open or create persistent local Chroma database
    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    # Open or create collection for support policy chunks
    collection = client.get_or_create_collection(
        name="support_policies"
    )

    return collection


def store_chunks(chunks):

    # Get ChromaDB collection
    collection = get_collection()

    for chunk in chunks:

        # Store or update one chunk in ChromaDB
        collection.upsert(
            ids=[chunk["chunk_id"]],
            documents=[chunk["text"]],
            embeddings=[chunk["embedding"]],
            metadatas=[chunk["metadata"]]
        )