import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import requests


def process_pdfs(upload_folder):
    docs = []

    for file in os.listdir(upload_folder):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(upload_folder, file))
            docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings()
    db = FAISS.from_documents(chunks, embeddings)

    db.save_local("vector_store")


def load_db():
    embeddings = HuggingFaceEmbeddings()
    return FAISS.load_local(
        "vector_store",
        embeddings,
        allow_dangerous_deserialization=True
    )


def ask_llm(query, db):
    docs = db.similarity_search(query, k=3)

    context = "\n\n".join([d.page_content for d in docs])
    sources = [d.metadata.get("source", "Unknown") for d in docs]

    prompt = f"""
You are a helpful assistant.

Answer ONLY from the given context.
If the answer is not clearly present, say: "Not in notes".

Context:
{context}

Question:
{query}
"""

    res = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    data = res.json()

    if "response" in data and data["response"].strip() != "":
        return data["response"], sources
    else:
        return "No valid answer found. Try rephrasing your question.", sources