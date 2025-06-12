import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Load the same embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load the ChromaDB directory
persist_directory = "vector_store/chroma_db"
vectordb = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding_model
)

# Simple query loop
while True:
    query = input("Ask a question about hotels in Skardu (or type 'exit' to quit): ")
    if query.lower() == "exit":
        break

    results = vectordb.similarity_search(query, k=3)

    print("\nTop 3 matching hotels:\n")
    for i, doc in enumerate(results, 1):
        print(f"Result {i}:\n{doc.page_content}\n{'-'*40}")
