# 🤖 Product Chatbot

A local Retrieval-Augmented Generation (RAG) chatbot powered by **Ollama (Llama3)** and **Streamlit**.

## 🚀 Features
- 100% offline chatbot using Ollama models
- RAG-based knowledge recall with ChromaDB
- Persistent chat memory using Streamlit session state

---

## 🧠 Setup Instructions

###1️⃣ Create virtual environment
```bash
git clone <your-repo-url>
cd PME_Chatbot

###2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate

###3️⃣ Install dependencies
pip install -r requirements.txt

###4️⃣ Pull the Ollama model
ollama pull llama3

###5️⃣ Run the Streamlit app
streamlit run app.py
