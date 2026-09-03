import streamlit as st
from config import TOP_K, CHUNK_SIZE, CHUNK_OVERLAP, GROQ_API_KEY
from pdf_reader import extract_text_from_pdf
from chunking import chunk_pages
from embeddings import get_embeddings_for_chunks
from retriever import build_vector_store, retrieve_relevant_chunks
from qa import generate_answer

def is_greeting(question):
    greetings = ["hi", "hello", "hey"]
    return question.lower().strip() in greetings

st.set_page_config(page_title="DocMind AI", layout="wide")
st.title("DocMind AI")
st.caption("Your intelligent document assistant")

if "chats" not in st.session_state:
    st.session_state.chats = []

if "current_chat" not in st.session_state:
    st.session_state.current_chat = -1

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "processed_files" not in st.session_state:
    st.session_state.processed_files = None

with st.sidebar:
    st.header("Chats")
    if st.button("📝 New Chat", use_container_width=True):
        st.session_state.current_chat = None
        st.rerun()
    st.divider()

    if st.session_state.chats:
        st.subheader("Previous Chats")
        for i,chat in enumerate(st.session_state.chats):
            if st.button(f"{chat['title']}",key=f"chat_{i}",use_container_width=True):
                st.session_state.current_chat = i
                st.rerun()
    st.divider()

    if st.button("Clear conversation", use_container_width=True):
        if st.session_state.current_chat is not None:
            st.session_state.chats[st.session_state.current_chat]["messages"] = []
        st.rerun()

uploaded_files = st.file_uploader("Upload your PDF(s)",type=["pdf"],accept_multiple_files=True)
if not uploaded_files:
    st.info("Upload a PDF to get started.")
    st.stop()

file_signature = tuple((file.name, file.size)for file in uploaded_files)

if st.session_state.processed_files != file_signature:
    with st.spinner("Reading and indexing your document(s)..."):
        all_chunks = []

        try:
            for file in uploaded_files:
                pages = extract_text_from_pdf(file)
                chunks = chunk_pages(pages,chunk_size=CHUNK_SIZE,overlap=CHUNK_OVERLAP,source_name=file.name)
                all_chunks.extend(chunks)
        except ValueError as e:
            st.error(str(e))
            st.stop()
        texts = []
        for chunk in all_chunks:
            texts.append(chunk["text"])
        embeddings = get_embeddings_for_chunks(texts)
        st.session_state.vector_store = build_vector_store(all_chunks,embeddings)
        st.session_state.processed_files = file_signature

    st.success(f"Indexed {len(all_chunks)} chunks "f"from {len(uploaded_files)} file(s).")

if st.session_state.current_chat == -1:
    st.session_state.chats.append({"title": "New Chat","messages": []})
    st.session_state.current_chat = len(st.session_state.chats) - 1

messages = st.session_state.chats[st.session_state.current_chat]["messages"]

def render_sources(sources):
    with st.expander("Sources"):
        for i, source in enumerate(sources, start=1):
            metadata = source.get("metadata", {})
            st.markdown(f"**Source {i}** — "f"{metadata.get('source', '?')}, "f"page {metadata.get('page', '?')} "f"(score: {source['score']:.3f})")
            st.write(source["chunk"])

for message in messages:
    with st.chat_message(message["role"],avatar="👨‍💻" if message["role"] == "user" else "✨"):
        st.write(message["content"])
        if message.get("sources"):
            render_sources(message["sources"])

question = st.chat_input("Ask anything about your document(s)...")
if question:
    chat = st.session_state.chats[st.session_state.current_chat]
    chat["messages"].append({"role": "user","content": question})

    if chat["title"] == "New Chat":
        chat["title"] = question[:30]

    with st.chat_message("user", avatar="👨‍💻"):
        st.write(question)

    with st.chat_message("assistant", avatar="✨"):
        if is_greeting(question):
            answer = "Hello! How can I help you with your document?"
            relevant_chunks = []
        else:
            with st.spinner("Thinking..."):
                relevant_chunks = retrieve_relevant_chunks(question,st.session_state.vector_store,top_k=TOP_K)
                if not relevant_chunks:
                    answer = "I could not find the answer in the document."
                else:
                    try:
                        answer = generate_answer(question,relevant_chunks)
                    except (ValueError, RuntimeError) as e:
                        answer = f"⚠️ {e}"

        st.write(answer)
        if relevant_chunks:
            render_sources(relevant_chunks)

    chat["messages"].append({"role": "assistant","content": answer,"sources": relevant_chunks})