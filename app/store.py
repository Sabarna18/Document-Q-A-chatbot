from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader, CSVLoader

class Store():

    def __init__(self):
        self.embeddings =  GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    def create_vector_db(self , documents):
        vectorstore = Chroma.from_documents(documents=documents , embedding=self.embeddings , persist_directory="Chroma_Store")
        return vectorstore
    
    def create_retriever(self , vectorstore):
        retriever = vectorstore.as_retriever( search_type="similarity" ,search_kwargs={"k":3})
        return retriever
    
    def save_file(self , file):
        save_dir = "uploaded_files"
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, file.name)
        with open (file_path , "wb") as f:
            f.write(file.getbuffer())
        return file_path