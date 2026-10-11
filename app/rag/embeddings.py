from app.config import client


def create_embedding(text):

    # Convert the given text into an embedding
    embedding_response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    # Extract and return the vector
    embedding = embedding_response.embeddings[0].values

    return embedding
  