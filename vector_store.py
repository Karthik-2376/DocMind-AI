# import numpy as np
# import faiss

# class VectorStore:
#     def __init__(self,chunk_embeddings,chunks):
#         embeddings = np.asarray(chunk_embeddings,dtype="float32")
#         self.dim = embeddings.shape[1]
#         self.index = faiss.IndexFlatIP(self.dim)
#         self.index.add(embeddings)
#         self.chunks = chunks 

#     def search(self,query_embedding,top_k=3):
#         query_embedding = np.asarray(query_embedding, dtype="float32").reshape(1, -1)
#         top_k = min(top_k,len(self.chunks))
#         scores,indices = self.index.search(query_embedding,top_k)
#         results = []
#         for score, idx in zip(scores[0], indices[0]):
#             if idx == -1:
#                 continue
#             chunk_meta = self.chunks[idx]
#             results.append({"chunk": chunk_meta["text"],"score": float(score),"metadata": chunk_meta,})
#         return results


import numpy as np
class VectorStore:
    def __init__(self,embeddings,chunks):
        self.embeddings = np.array(embeddings)
        self.chunks = chunks
        
    def search(self,query_embedding,top_k=3):
        query_embedding = np.array(query_embedding)
        scores = []
        for i,embedding in enumerate(self.embeddings):
            similarity = np.dot(query_embedding, embedding) / (
                np.linalg.norm(query_embedding) *
                np.linalg.norm(embedding)
            )
            scores.append((similarity, i))
        scores.sort(reverse=True)
        results = []
        for score, index in scores[:top_k]:
            results.append({"chunk": self.chunks[index]["text"],"score": float(score),"metadata": self.chunks[index]})

        return results