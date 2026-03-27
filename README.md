# SAP Project
# College Notes Assistant (Local GPT)

An AI-powered system that allows users to upload PDF notes and ask questions using a local language model.


##  Features
-  PDF-based Question Answering  
-  Fast retrieval using FAISS  
-  Local AI model (LLaMA 3 via Ollama)  
-  Works offline after setup  
-  Context-based answers (no hallucination)  

---

## How It Works

1. Upload PDF  
2. Text is extracted  
3. Split into chunks  
4. Converted into embeddings  
5. Stored in FAISS  
6. Query retrieves relevant chunks  
7. LLM generates answer  

---

## Tech Stack

- Python  
- Streamlit  
- LangChain  
- FAISS  
- Ollama (LLaMA 3)  

---

## Run the Project

```bash
streamlit run app.py
