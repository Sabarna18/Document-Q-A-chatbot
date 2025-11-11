import streamlit as st
import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader, CSVLoader

def save_uploaded_file(uploaded_file):
    """Save the uploaded file to a temporary directory."""
    save_dir = "uploaded_files"
    os.makedirs(save_dir, exist_ok=True)
    
    file_path = os.path.join(save_dir, uploaded_file.name)
    
    # Write the file to disk
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path


def main():
    st.title("LangChain File Loader Demo")

    uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx", "csv"])

    if uploaded_file is not None:
        # Save file locally
        saved_path = (save_uploaded_file(uploaded_file))
        st.success(f"✅ File saved at: {saved_path}")
        

        # Load using the correct LangChain Loader
        if uploaded_file.name.endswith(".txt"):
            loader = TextLoader(saved_path)
        elif uploaded_file.name.endswith(".pdf"):
            loader = TextLoader(saved_path)
        elif uploaded_file.name.endswith(".docx"):
            loader = TextLoader(saved_path)
        elif uploaded_file.name.endswith(".csv"):
            loader = CSVLoader(saved_path)
        else:
            st.error("❌ Unsupported file format.")
            return

        # Load data into LangChain Documents
        data = loader.load()

        st.write("📄 **Loaded Data Sample:**")
        st.write(data[0].page_content[:500])  # Show first 500 chars of content

        # You can now use `data` for embeddings, retrievers, etc.


if __name__ == "__main__":
    main()
