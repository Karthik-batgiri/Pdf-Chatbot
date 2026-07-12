# Generated from: ingest.ipynb
# Converted at: 2026-07-10T16:38:54.219Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS




def ingest_pdf(file_path):


    # Load PDF

    loader = PyPDFLoader(file_path)
    docs = loader.load()

    print(f"Loaded PDF: {file_path}")
    print(f"Pages: {len(docs)}")
    
    # Split Documents
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(docs)

    print(f"Chunks Created: {len(chunks)}")


    # Embedding Model

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    
    # Create Vector Store
    
    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    
    # Save Vector Store
    
    vectorstore.save_local("faiss_index")

    print("FAISS Index Saved Successfully!")

    return True