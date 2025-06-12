import pandas as pd
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
import os

# Load hotel data
df = pd.read_csv("data/skardu_hotels.csv")
df.columns = df.columns.str.strip()  # Clean column names just in case

# Combine relevant fields into one string per row
df['combined'] = df.apply(
    lambda row: (
        f"Name: {row['hotel_name']}\n"
        f"Location: {row['location']}\n"
        f"City: {row['city']}\n"
        f"Rating: {row['rating']}\n"
        f"Price: {row['price']}\n"
        f"URL: {row['url']}"
    ),
    axis=1
)

# Convert to Langchain Document objects
documents = [Document(page_content=text) for text in df['combined']]

# Split long texts (not really needed here but keeps things consistent)
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# Initialize HuggingFace embeddings
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Store in Chroma vector DB (stored in ./vector_store/chroma_db/)
vector_store = Chroma.from_documents(texts, embedding_model, persist_directory="vector_store/chroma_db")
vector_store.persist()

print("✅ Hotel data embedded and stored in ChromaDB.")