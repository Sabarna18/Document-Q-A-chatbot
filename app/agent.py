from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import TextLoader , PyPDFLoader, Docx2txtLoader, CSVLoader
from langchain_core.documents import Document
import tempfile , fitz
import os
from tika import parser

load_dotenv()

class Agent():
    
    def __init__(self):
        self.groq_llm = ChatGroq(model="llama-3.3-70b-versatile" , temperature=0.5 , timeout=5000)
        self.gemini_model = init_chat_model("google_genai:gemini-2.5-flash" , temperature=0.5)   
        
    def load_doc(self, saved_path, uploaded_file ):
        """Test function to load and return content from an uploaded file."""
        if uploaded_file.name.endswith(".txt"):
            loader = TextLoader(saved_path , encoding='utf-8' ,autodetect_encoding=True)
        elif uploaded_file.name.endswith(".pdf"):
            loader = TextLoader(saved_path , encoding='utf-8' ,autodetect_encoding=True)
            raw = parser.from_file(saved_path )
            data = Document(page_content=raw['content'] , metadata={"source": saved_path})
            return [data]
        elif uploaded_file.name.endswith(".docx"):
            loader = TextLoader(saved_path , encoding='utf-8' ,autodetect_encoding=True)
        elif uploaded_file.name.endswith(".csv"):
            loader = CSVLoader(saved_path)
        else:
            return

        # Load data into LangChain Documents
        data = loader.load()
        return data 
    
    def test_load_doc(self , saved_path , uploaded_file):
        doc = fitz.open(saved_path)
        text = ""
        for page_num, page in enumerate(doc):
            text += f"\n--- Page {page_num + 1} ---\n"
            text += page.get_text()
        doc.close()

        data = Document(page_content=text , metadata={"source": saved_path})  
        return [data]     
            
    def format_docs(self , docs):
        return "\n\n".join([doc.page_content for doc in docs])

    
    def generate_answer(self , retriever , model , question):
        template = '''answer the question based on the context below.If the answer is not contained within the text, respond with "I don't know". 
        context : {context}
        question: {question}
        answer:         '''
        prompt = PromptTemplate.from_template(template)
        
        rag_chain = (
            {"context": retriever | self.format_docs , "question": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
        )
        answer = rag_chain.invoke(question)
        return answer