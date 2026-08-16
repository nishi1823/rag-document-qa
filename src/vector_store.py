import faiss
import numpy as np


def create_vector_store(embeddings):
    """
    Create a FAISS vector index from embeddings.
    """

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(embeddings)

    return index


def search_vector_store(
    index,
    query_embedding,
    text_chunks,
    top_k=3
):
    """
    Search the FAISS index and return
    the most relevant text chunks.
    """

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    scores, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for score, index_position in zip(
        scores[0],
        indices[0]
    ):

        if index_position == -1:
            continue

        results.append(
            {
                "text": text_chunks[index_position],
                "score": float(score)
            }
        )

    return results