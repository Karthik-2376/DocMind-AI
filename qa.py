from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

def _build_prompt(question,relevant_chunks):
    context_parts = []
    for i,item in enumerate(relevant_chunks,start=1):
        meta = item.get("metadata", {})
        page = meta.get("page", "?")
        source = meta.get("source", "document")
        context_parts.append(f"[Source {i} | {source}, page {page}]\n{item['chunk']}")
    context = "\n\n".join(context_parts)

    return f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the information provided in the context.

Rules:
- Do not use outside knowledge.
- Give a clear and direct answer.
- Do not mention the context, chunks, sources, or retrieval process.
- Do not add information that is not present in the context.
- If the answer cannot be found in the context, say:
  "I could not find the answer in the document."

Context:
{context}

Question:
{question}

Answer:
"""


def generate_answer(question, relevant_chunks):
    prompt = _build_prompt(question, relevant_chunks)
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(model=GROQ_MODEL,messages=[{"role": "user", "content": prompt}],temperature=0.1)
    return response.choices[0].message.content.strip()
 
