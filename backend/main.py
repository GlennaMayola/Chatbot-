import os
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# Load API Key
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Store vector DB globally
vectorstore = None

@app.get("/")
async def root():
    return {"message": "PDF Chat API is running!"}

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    global vectorstore

    try:
        # Save uploaded PDF temporarily
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Load and process PDF
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(documents)

        # Use free HuggingFace embeddings
        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

        # Store in FAISS vector DB
        vectorstore = FAISS.from_documents(docs, embeddings)

        # Clean up temp file
        if os.path.exists(file_path):
            os.remove(file_path)

        return {"message": "✅ PDF uploaded and processed successfully!"}
    
    except Exception as e:
        print(f"Error in upload_pdf: {str(e)}")
        return {"error": str(e)}

@app.post("/ask/")
async def ask_question(query: str = Form(...)):
    global vectorstore
    
    try:
        if vectorstore is None:
            return {"answer": "⚠️ Please upload a PDF first."}

        retriever = vectorstore.as_retriever()

        # Groq LLM - Using latest available model
        llm = ChatGroq(
            groq_api_key=groq_api_key,
            model="llama-3.3-70b-versatile",  # Latest model as of Oct 2024
            temperature=0
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff"
        )

        result = qa_chain.run(query)
        return {"answer": result}
    
    except Exception as e:
        print(f"Error in ask_question: {str(e)}")
        return {"error": str(e)}