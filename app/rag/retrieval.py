from app.rag.embeddings import create_embedding
from app.rag.vector_store import get_collection


def retrieve_chunks(question, product, top_k=3):

    # Convert user's question into embedding
    query_embedding = create_embedding(question)

    # Access stored policy collection
    collection = get_collection()

    # Search only active policies
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={
    "$and": [
        {"status": "active"},
        {
            "$or": [
                {"product": product},
                {"product": "all_products"}
            ]
        }
    ]
},
        include=["documents", "metadatas", "distances"]
    )

    # Maximum distance we currently accept
    max_distance = 0.75

    retrieved_chunks = []

    # Check every retrieved result
    for i in range(len(results["documents"][0])):

        distance = results["distances"][0][i]

        # Ignore weak retrieval results
        if distance > max_distance:
            continue
       

        # Keep relevant chunk
        retrieved_chunks.append({
            "chunk_id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": distance
        })

    # Return only after checking all results
    return retrieved_chunks