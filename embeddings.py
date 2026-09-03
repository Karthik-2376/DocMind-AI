import streamlit as st
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL_NAME

@st.cache_resource(show_spinner=False)

def load_embedding_model():
    return SentenceTransformer(EMBEDDING_MODEL_NAME)

def get_embedding(text):
    model = load_embedding_model()
    return model.encode(text, normalize_embeddings=True)

def get_embeddings_for_chunks(chunk_texts):
    model = load_embedding_model()
    return model.encode(chunk_texts,normalize_embeddings=True,show_progress_bar=False,)
