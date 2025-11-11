import streamlit as st
from store import Store
from agent import Agent
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader, CSVLoader

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Document Q&A",
    page_icon="🤖",
    layout="centered"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #1f1c2c, #928DAB);
            color: white;
        }
        .main {
            background: rgba(255, 255, 255, 0.07);
            backdrop-filter: blur(12px);
            padding: 2rem 3rem;
            border-radius: 20px;
            box-shadow: 0px 8px 25px rgba(0,0,0,0.25);
        }
        .stTextInput > div > div > input {
            color: #000;
            background-color: #f1f1f1;
            border-radius: 8px;
            padding: 8px;
        }
        .stButton > button {
            background: linear-gradient(90deg, #ff416c, #ff4b2b);
            color: white;
            border: none;
            padding: 0.6rem 1.2rem;
            border-radius: 10px;
            font-weight: bold;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            transform: scale(1.05);
            background: linear-gradient(90deg, #ff4b2b, #ff416c);
        }
        .answer-box {
            background-color: rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 1rem;
            margin-top: 1rem;
            font-size: 1.05rem;
            color: #f0f0f0;
        }
    </style>
""", unsafe_allow_html=True)


# ---------- MAIN FUNCTION ----------
def main():
    st.markdown("<h1 style='text-align:center;'>🤖 Welcome to AI Document Q&A</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:1.1rem;'>Upload your text file and ask any question about it!</p>", unsafe_allow_html=True)

    with st.container():
        enter_doc = st.file_uploader("📂 Upload a document ", type=["txt" , "pdf" , "docx" , "csv"])
        question = st.text_input("💬 Enter your question about the document:")
        submit_btn = st.button("🚀 Get Answer")
    
    if enter_doc is not None:
        
        st.success(f"✅ File '{enter_doc.name}' uploaded successfully!")

    if submit_btn:
        if not enter_doc:
            st.warning("⚠️ Please upload a document first.")
            return

        if not question.strip():
            st.warning("⚠️ Please enter a question.")
            return

        agent = Agent()
        store = Store()
        

        with st.spinner("🔍 Processing document and generating answer..."):
            file_path = store.save_file(file=enter_doc)
            document = agent.load_doc(saved_path=file_path, uploaded_file=enter_doc)
            vectorstore = store.create_vector_db(documents=document)
            retriever = store.create_retriever(vectorstore=vectorstore)
            model = agent.model
            answer = agent.generate_answer(retriever=retriever, model=model, question=question)

        st.success("✅ Answer generated successfully!")

        # Display the result in a nice styled box
        st.markdown("<div class='answer-box'><strong>Answer:</strong><br>" + answer + "</div>", unsafe_allow_html=True)


# ---------- RUN ----------
if __name__ == "__main__":
    main()
