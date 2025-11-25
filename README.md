# 🤖 Product Chatbot

A local **Retrieval-Augmented Generation (RAG)** chatbot powered by **Ollama (Llama3)** and **Streamlit**, designed for fast, offline, and intelligent product support.

---

## 🚀 Features

- 💬 **100% offline chatbot** using local Ollama models  
- 🧠 **RAG-based knowledge grounding** using ChromaDB  
- 🔍 **Cross Encoder re-ranking** for highly accurate retrieval  
- 🗂️ **Persistent chat memory** using Streamlit session state  
- 🧩 **Modular architecture** to avoid circular loops and repeated model downloads  
- ⚡ Fast, simple setup and fully local processing  

---

## 🔍 Enhanced Retrieval System

To ensure top-quality responses, the chatbot uses a **Cross Encoder** to re-rank retrieved document chunks before sending them to the LLM.

### ✅ Benefits of the Cross Encoder

- Improved semantic matching between user query and documents  
- More accurate and relevant context retrieval  
- Reduced hallucinations  
- Ideal for documents with many similar or overlapping sentences  

---

## 🛡️ Modular Architecture (Avoid Circular Loops)

The project uses **separate files** for:

- ⬇️ Model downloading (Ollama, embedding models)  
- 📚 Embedding generation  
- 🔎 Cross encoder scoring  
- 💬 LLM response generation  
- 🧠 Memory management  
- 🎯 Retrieval pipeline  

This structure ensures:

- 🚫 No repeated model downloads  
- 🚫 No circular imports  
- ⚡ Smooth startup  
- 🧼 Cleaner and maintainable codebase  

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2️⃣ Create and Activate Virtual Environment

```bash
python -m venv venv
```

*   On **Windows**:
    ```bash
    .\venv\Scripts\activate
    ```

*   On **macOS/Linux**:
    ```bash
    source venv/bin/activate
    ```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Pull the Ollama Model

```bash
ollama pull llama3
```

### 5️⃣ Run the Streamlit App

```bash
streamlit run app.py
```

***

## 📝 Notes

- Ensure **Ollama** is installed and running locally.  
- The chatbot uses **ChromaDB** for vector storage.  
- Chat history is stored using **Streamlit session state**.  
- A **Cross Encoder** is used for high-quality chunk re-ranking.  
- Models are downloaded in a **dedicated file**, preventing circular loops and redundant downloads.

