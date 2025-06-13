import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# --- Load data ---
df = pd.read_csv("data/skardu_hotels.csv")  # Replace with your real file name

# --- Prepare text documents ---
def row_to_text(row):
    return f"{row['hotel_name']} in {row['location']} | Price: {row['price']} | City: {row['city']}"

docs = df.apply(row_to_text, axis=1).tolist()

# --- Load embedding model ---
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# --- Embed hotel descriptions ---
print("🔄 Embedding hotel descriptions...")
embeddings = model.encode(docs, convert_to_numpy=True)

# --- Create FAISS index ---
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

# --- Simple query loop ---
def search_hotels(user_query, top_k=5):
    query_embedding = model.encode([user_query])
    D, I = index.search(query_embedding, top_k)
    print(f"\n📍 Top {top_k} hotels for query: '{user_query}':\n")
    for idx in I[0]:
        print(f"🏨 {docs[idx]}")
        print(f"📅 Schedule: https://calendly.com/your-schedule-link")  # Placeholder
        print("---")

if __name__ == "__main__":
    while True:
        query = input("\n🔎 Enter your hotel search query (or 'exit'): ")
        if query.lower() in ["exit", "quit"]:
            break
        search_hotels(query)
