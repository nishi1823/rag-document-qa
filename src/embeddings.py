from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


model = SentenceTransformer(
    MODEL_NAME
)


def create_embeddings(text_chunks):
    """
    Convert text chunks into numerical embeddings.
    """

    embeddings = model.encode(
        text_chunks,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings


def create_query_embedding(query):
    """
    Convert a user question into an embedding.
    """

    embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embedding