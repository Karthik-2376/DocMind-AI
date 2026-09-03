def chunk_pages(pages,chunk_size=150,overlap=30,source_name="document"):
    chunks = []
    chunk_id = 0
    for page_info in pages:
        page_num = page_info["page"]
        words = page_info["text"].split()
        start = 0
        while start < len(words):
            end = start + chunk_size
            chunk_words = words[start:end]
            chunks.append({"chunk_id": chunk_id,"text": " ".join(chunk_words),"page": page_num,"source": source_name,})
            chunk_id += 1
            if end >= len(words):
                break
            start = end - overlap

    return chunks


def chunk_text(text,chunk_size=150,overlap=30):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        if end >= len(words):
            break
        start = end - overlap
        
    return chunks
