import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
GROQ_MODEL = st.secrets.get("GROQ_MODEL", os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"))
EMBEDDING_MODEL_NAME = st.secrets.get("EMBEDDING_MODEL_NAME", os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2"))
CHUNK_SIZE = int(st.secrets.get("CHUNK_SIZE", os.getenv("CHUNK_SIZE", 150)))
CHUNK_OVERLAP = int(st.secrets.get("CHUNK_OVERLAP", os.getenv("CHUNK_OVERLAP", 30)))
TOP_K = int(st.secrets.get("TOP_K", os.getenv("TOP_K", 5)))
