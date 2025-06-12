import os
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFaceHub

# Load environment variables
load_dotenv()

# Load Hugging Face API key from environment
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Load vector store
vectorstore = FAISS.load_local("vector_store/hotel_faiss_index", HuggingFaceEmbeddings(), allow_dangerous_deserialization=True)

# Load the Hugging Face model (flan-t5-base)
llm = HuggingFaceHub(
    repo_id="google/flan-t5-base",  # Available on HuggingFace inference API
    model_kwargs={"temperature": 0.5, "max_length": 512}
)

# Create RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever()
)

# CLI loop
print("Ask a question about hotels in Skardu (type 'exit' to quit):\n")
while True:
    query = input("> ")
    if query.lower() == "exit":
        break
    result = qa_chain.invoke({"query": query})
    print(f"\nAnswer: {result['result']}\n")