import streamlit as st
from store import Store
from agent import Agent
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader, CSVLoader
import time

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Document Intelligence Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- PROFESSIONAL CUSTOM CSS ----------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        /* Main Background */
        .stApp {
            background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
        }
        
        /* Remove default padding */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }
        
        /* Hero Section */
        .hero-section {
            text-align: center;
            padding: 4rem 2rem 3rem 2rem;
            animation: fadeInDown 1s ease-out;
        }
        
        .hero-title {
            font-size: 4rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 1rem;
            letter-spacing: -2px;
            line-height: 1.1;
        }
        
        .hero-subtitle {
            font-size: 1.4rem;
            color: rgba(255, 255, 255, 0.8);
            font-weight: 300;
            max-width: 700px;
            margin: 0 auto 2rem auto;
            line-height: 1.6;
        }
        
        .hero-badge {
            display: inline-block;
            background: rgba(102, 126, 234, 0.2);
            color: #a8b2ff;
            padding: 0.5rem 1.5rem;
            border-radius: 50px;
            font-size: 0.9rem;
            font-weight: 600;
            border: 1px solid rgba(102, 126, 234, 0.3);
            margin-bottom: 2rem;
            animation: pulse 2s ease-in-out infinite;
        }
        
        /* Stats Bar */
        .stats-container {
            display: flex;
            justify-content: center;
            gap: 3rem;
            margin: 3rem 0;
            flex-wrap: wrap;
            animation: fadeInUp 1s ease-out 0.3s both;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .stat-label {
            font-size: 0.9rem;
            color: rgba(255, 255, 255, 0.6);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 0.5rem;
        }
        
        /* Main Content Card */
        .main-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(30px);
            -webkit-backdrop-filter: blur(30px);
            border-radius: 30px;
            padding: 3rem;
            margin: 2rem auto;
            max-width: 900px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            animation: fadeInUp 1s ease-out 0.5s both;
        }
        
        /* Feature Grid */
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 3rem 0;
            animation: fadeInUp 1s ease-out 0.4s both;
        }
        
        .feature-card {
            background: rgba(255, 255, 255, 0.03);
            padding: 2rem;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
        }
        
        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transform: scaleX(0);
            transition: transform 0.4s ease;
        }
        
        .feature-card:hover::before {
            transform: scaleX(1);
        }
        
        .feature-card:hover {
            background: rgba(255, 255, 255, 0.08);
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
            border-color: rgba(102, 126, 234, 0.3);
        }
        
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            display: block;
            filter: grayscale(0.3);
            transition: all 0.3s ease;
        }
        
        .feature-card:hover .feature-icon {
            filter: grayscale(0);
            transform: scale(1.1) rotateZ(5deg);
        }
        
        .feature-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: white;
            margin-bottom: 0.8rem;
        }
        
        .feature-description {
            font-size: 0.95rem;
            color: rgba(255, 255, 255, 0.6);
            line-height: 1.6;
        }
        
        /* File Uploader Styling */
        .stFileUploader {
            margin: 2rem 0;
        }
        
        .stFileUploader > label {
            color: white !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            margin-bottom: 1rem !important;
        }
        
        .stFileUploader > div {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 2px dashed rgba(102, 126, 234, 0.4) !important;
            border-radius: 20px !important;
            padding: 3rem !important;
            transition: all 0.4s ease !important;
        }
        
        .stFileUploader > div:hover {
            background: rgba(255, 255, 255, 0.08) !important;
            border-color: rgba(102, 126, 234, 0.8) !important;
            transform: scale(1.02);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.2);
        }
        
        /* Text Input Styling */
        .stTextInput > label {
            color: white !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            margin-bottom: 1rem !important;
        }
        
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.08) !important;
            color: white !important;
            border: 2px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 15px !important;
            padding: 1rem 1.5rem !important;
            font-size: 1.05rem !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: rgba(255, 255, 255, 0.4) !important;
        }
        
        .stTextInput > div > div > input:focus {
            background: rgba(255, 255, 255, 0.12) !important;
            border-color: #667eea !important;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.2) !important;
            transform: translateY(-2px);
        }
        
        /* Button Styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 1rem 3rem;
            border-radius: 15px;
            font-weight: 700;
            font-size: 1.1rem;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            width: 100%;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
            position: relative;
            overflow: hidden;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.5s;
        }
        
        .stButton > button:hover::before {
            left: 100%;
        }
        
        .stButton > button:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 20px 50px rgba(102, 126, 234, 0.6);
        }
        
        .stButton > button:active {
            transform: translateY(-2px) scale(0.98);
        }
        
        /* Answer Box */
        .answer-container {
            animation: fadeInUp 0.8s ease-out;
        }
        
        .answer-box {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            border-radius: 25px;
            padding: 2.5rem;
            margin-top: 2rem;
            border: 2px solid rgba(102, 126, 234, 0.3);
            box-shadow: 0 15px 50px rgba(0, 0, 0, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .answer-box::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2, #667eea);
            background-size: 200% 100%;
            animation: shimmer 3s linear infinite;
        }
        
        .answer-header {
            font-size: 1.5rem;
            font-weight: 700;
            color: white;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }
        
        .answer-content {
            font-size: 1.1rem;
            color: rgba(255, 255, 255, 0.9);
            line-height: 1.9;
            font-weight: 400;
        }
        
        /* Success/Warning Messages */
        .stSuccess {
            background: rgba(76, 209, 55, 0.15) !important;
            border-left: 4px solid #4cd137 !important;
            border-radius: 12px !important;
            animation: slideInRight 0.5s ease-out;
        }
        
        .stWarning {
            background: rgba(255, 193, 7, 0.15) !important;
            border-left: 4px solid #ffc107 !important;
            border-radius: 12px !important;
            animation: shake 0.5s ease-out;
        }
        
        /* Spinner */
        .stSpinner > div {
            border-top-color: #667eea !important;
            border-right-color: #764ba2 !important;
        }
        
        /* Animations */
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
                opacity: 1;
            }
            50% {
                transform: scale(1.05);
                opacity: 0.8;
            }
        }
        
        @keyframes shimmer {
            0% {
                background-position: -200% 0;
            }
            100% {
                background-position: 200% 0;
            }
        }
        
        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(50px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }
        
        /* Divider */
        .custom-divider {
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.5), transparent);
            margin: 3rem 0;
            animation: shimmer 3s linear infinite;
            background-size: 200% 100%;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .hero-title {
                font-size: 2.5rem;
            }
            
            .hero-subtitle {
                font-size: 1.1rem;
            }
            
            .main-card {
                padding: 2rem 1.5rem;
            }
            
            .stats-container {
                gap: 1.5rem;
            }
            
            .stat-number {
                font-size: 2rem;
            }
        }
    </style>
""", unsafe_allow_html=True)


# ---------- MAIN FUNCTION ----------
def main():
    # Hero Section
    st.markdown("""
        <div class='hero-section'>
            <div class='hero-badge'>✨ Powered by Advanced AI Technology</div>
            <h1 class='hero-title'>Document Intelligence Platform</h1>
            <p class='hero-subtitle'>Transform your documents into intelligent conversations. Upload, ask, and get instant AI-powered insights from any document format.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Stats Section
    st.markdown("""
        <div class='stats-container'>
            <div class='stat-item'>
                <div class='stat-number'>4+</div>
                <div class='stat-label'>File Formats</div>
            </div>
            <div class='stat-item'>
                <div class='stat-number'>∞</div>
                <div class='stat-label'>Questions</div>
            </div>
            <div class='stat-item'>
                <div class='stat-number'>&lt;2s</div>
                <div class='stat-label'>Avg Response Time</div>
            </div>
            <div class='stat-item'>
                <div class='stat-number'>99%</div>
                <div class='stat-label'>Accuracy Rate</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Feature Grid
    st.markdown("""
        <div class='feature-grid'>
            <div class='feature-card'>
                <span class='feature-icon'>📄</span>
                <div class='feature-title'>Multi-Format Support</div>
                <div class='feature-description'>Process PDF, TXT, DOCX, and CSV files seamlessly with advanced parsing capabilities.</div>
            </div>
            <div class='feature-card'>
                <span class='feature-icon'>🧠</span>
                <div class='feature-title'>AI-Powered Analysis</div>
                <div class='feature-description'>Leveraging state-of-the-art language models for contextual understanding.</div>
            </div>
            <div class='feature-card'>
                <span class='feature-icon'>⚡</span>
                <div class='feature-title'>Lightning Fast</div>
                <div class='feature-description'>Vector-based search delivers instant answers from massive documents.</div>
            </div>
            <div class='feature-card'>
                <span class='feature-icon'>🔒</span>
                <div class='feature-title'>Secure & Private</div>
                <div class='feature-description'>Your documents are processed securely with enterprise-grade protection.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Custom Divider
    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
    
    # Main Card
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    
    # File Upload Section
    enter_doc = st.file_uploader(
        "📂 Upload Your Document",
        type=["txt", "pdf", "docx", "csv"],
        help="Drag and drop or click to browse • Max file size: 200MB"
    )
    
    # Success message for file upload
    if enter_doc is not None:
        st.success(f"✅ **{enter_doc.name}** uploaded successfully! ({enter_doc.size / 1024:.2f} KB)")
    
    # Question Input
    question = st.text_input(
        "💬 What would you like to know?",
        placeholder="e.g., Summarize the key points, What are the main findings?, Extract specific information...",
        help="Ask any question about the content of your uploaded document"
    )
    
    # Submit Button
    submit_btn = st.button("🚀 Generate AI Answer")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Process and Generate Answer
    if submit_btn:
        if not enter_doc:
            st.warning("⚠️ Please upload a document first to continue.")
            return

        if not question.strip():
            st.warning("⚠️ Please enter a question to get your answer.")
            return

        agent = Agent()
        store = Store()
        
        with st.spinner("🔍 Analyzing document and generating intelligent response..."):
            file_path = store.save_file(file=enter_doc)
            document = agent.load_doc(saved_path=file_path, uploaded_file=enter_doc)
            vectorstore = store.create_vector_db(documents=document)
            retriever = store.create_retriever(vectorstore=vectorstore)
            model = agent.groq_llm
            answer = agent.generate_answer(retriever=retriever, model=model, question=question)
        
        st.success("✅ Answer generated successfully!")
        
        # Display Answer in Professional Box
        st.markdown("<div class='answer-container'>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class='answer-box'>
                <div class='answer-header'>
                    <span>💡</span>
                    <span>AI-Generated Answer</span>
                </div>
                <div class='answer-content'>{answer}</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ---------- RUN ----------
if __name__ == "__main__":
    main()