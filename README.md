# 🤖 Product Chatbot

A local Retrieval-Augmented Generation (RAG) chatbot powered by **Ollama (Llama3)** and **Streamlit**.

***

## 🚀 Features

*   💬 100% offline chatbot using Ollama models
*   🧠 RAG-based knowledge recall with ChromaDB
*   🗂️ Persistent chat memory using Streamlit session state

***

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

*   Ensure Ollama is installed and running locally.
*   The chatbot uses **ChromaDB** for local vector storage.
*   All chat history is stored using **Streamlit's session state**, ensuring persistence across interactions.
*   You can add your own data to the guide folder

