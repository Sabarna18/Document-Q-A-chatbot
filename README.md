📘 Document Q&A Chatbot
Ask questions directly from your documents using AI

🚀 Overview

Document Q&A Chatbot is an AI-powered application that lets users upload documents (PDF, TXT, DOCX, CSV) and interact with them through natural language queries.
Using LangChain, Groq API, and Streamlit, it builds a retrieval-augmented generation (RAG) pipeline to find and summarize answers directly from your uploaded content — no need to read entire files manually.

🧩 Key Features

📁 Upload Documents: Supports .pdf, .txt, .docx, and .csv files.

🧠 Contextual Q&A: Ask any question and get relevant answers grounded in your document content.

⚡ Groq-Powered LLM: Uses Groq API for lightning-fast inference.

🔍 Smart Chunking & Retrieval: Efficiently splits and indexes document text for precise answer extraction.

💬 Streamlit Frontend: Clean, interactive chat interface for document upload and query interaction.

🗂️ Multi-File Support (optional): Easily extendable to multiple document uploads.

🧱 Tech Stack
Component	Description
Python	Core language
LangChain	Manages document loading, chunking, embedding, and retrieval
Groq API	Large Language Model (LLM) backend
Streamlit	User interface for uploading files and chatting
ChromaDB / FAISS	Vector database for storing embeddings (depending on setup)
📂 Project Structure
📦 document-qa-chatbot
├── app.py                  # Main Streamlit app
├── requirements.txt        # Dependencies
├── store.py                # Handles vectorstore creation/loading
├── agent.py                # LLM + Retriever logic
├── uploaded_files/         # Folder for saved uploads
├── README.md               # Project documentation

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/<your-username>/document-qa-chatbot.git
cd document-qa-chatbot

2️⃣ Create a Virtual Environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Set Up Environment Variables

Create a .env file in the project root and add your Groq API key:

GROQ_API_KEY=your_groq_api_key_here

5️⃣ Run the App
streamlit run app.py


Then open your browser at http://localhost:8501
 🎉

🧠 How It Works

Upload a Document → The file is saved locally and processed with LangChain document loaders.

Text Splitting → Long text is chunked into manageable pieces for embedding.

Vector Store Creation → Each chunk is converted into embeddings and stored in Chroma or FAISS.

Retriever + LLM Pipeline → When you ask a question, relevant chunks are retrieved and passed to the Groq LLM.

Answer Generation → The model returns a concise, context-aware answer sourced from your document.

🧩 Example Workflow

Upload a research paper (e.g., ai_research.pdf)

Type:

What are the main findings of the study?


The chatbot extracts context and responds:

The study concludes that fine-tuned transformers outperform standard models in low-data regimes.