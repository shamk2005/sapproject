import streamlit as st
import os
import shutil
from utils import process_pdfs, load_db, ask_llm

st.set_page_config(page_title="Notes Assistant", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []

st.title("📚 College Notes Assistant (Local GPT)")

uploaded_files = st.file_uploader("Upload PDFs", accept_multiple_files=True)

if uploaded_files:
    # 🔴 FULL RESET (this was your missing piece)
    if os.path.exists("uploads"):
        shutil.rmtree("uploads")

    if os.path.exists("vector_store"):
        shutil.rmtree("vector_store")

    os.makedirs("uploads", exist_ok=True)

    for file in uploaded_files:
        with open(f"uploads/{file.name}", "wb") as f:
            f.write(file.getbuffer())

    process_pdfs("uploads")

    st.success("Files processed successfully!")

query = st.text_input("Ask a question from your notes:")

if query:
    db = load_db()
    answer, sources = ask_llm(query, db)

    st.session_state.history.append((query, answer, sources))

for q, a, s in st.session_state.history[::-1]:
    st.markdown(f"### ❓ {q}")
    st.markdown(f"**Answer:** {a}")
    st.markdown(f"📄 Sources: {set(s)}")