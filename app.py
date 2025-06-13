# app.py
import streamlit as st
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# --- Load model, docs, index ---
@st.cache_resource
def load_resources():
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    index = faiss.read_index("faiss_index/index.bin")
    with open("faiss_index/docs.pkl", "rb") as f:
        docs = pickle.load(f)
    return model, index, docs

model, index, docs = load_resources()

# --- Search Function ---
def search_hotels(user_query, top_k=5):
    query_embedding = model.encode([user_query])
    D, I = index.search(np.array(query_embedding), top_k)
    results = [docs[i] for i in I[0]]
    return results

# --- Streamlit UI ---
st.title("🏨 Hotel Finder for Skardu")
st.markdown("Search hotels and schedule a call 📅")

user_query = st.text_input("🔎 Enter your hotel search query")

if user_query:
    with st.spinner("Searching hotels..."):
        results = search_hotels(user_query)
        for hotel in results:
            st.write("🏨", hotel)
            st.markdown("[📅 Schedule](https://calendly.com/your-schedule-link)", unsafe_allow_html=True)
            st.markdown("---")