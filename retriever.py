from embeddings import get_embedding
from vector_store import VectorStore


def build_vector_store(chunks,chunk_embeddings):
    return VectorStore(chunk_embeddings,chunks)

def retrieve_relevant_chunks(query,vector_store,top_k=3,threshold=0.5):
    query_embedding = get_embedding(query)
    results = vector_store.search(query_embedding,top_k=top_k)
    relevant_results = []
    for result in results:
        if result["score"] >= threshold:
            relevant_results.append(result)

    return relevant_results
