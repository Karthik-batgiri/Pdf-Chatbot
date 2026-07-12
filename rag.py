# Generated from: rag.ipynb
# Converted at: 2026-07-10T16:39:36.931Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_google_genai import ChatGoogleGenerativeAI
import os

os.environ["GOOGLE_API_KEY"] = "####"


def ask_question(question):

    # Handle greetings without RAG
  

    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    if question.lower().strip() in greetings:
        return "Hello! 👋 How can I help you today?"

   
    # Load Embedding Model
   

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

   
    # Load Latest FAISS Index
    vectorstore = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    # Create Retriever   
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k":3}
    )

    
    # Load LLM

    # llm = ChatOllama(
    #     model="llama3"
    # )

    llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)
    
    # Prompt
    prompt = ChatPromptTemplate.from_template("""


Rules:
You are a helpful AI assistant.

Use the provided context whenever it contains information relevant to the user's question.

Instructions:

If the context contains the answer, answer using the information from the context.
If the context does not contain the answer, use your own general knowledge to answer the question.
Do not claim that information came from the document unless it actually did.
If you are unsure or do not know the answer, say so instead of making up information.
Keep your responses clear, accurate, and concise.

Context:

Context:
{context}

Question:
{input}

Answer:
""")


    # Document Chain

    document_chain = create_stuff_documents_chain(
        llm,
        prompt
    )

    
    # Retrieval Chain
    retrieval_chain = create_retrieval_chain(
        retriever,
        document_chain
    )


    
    # Generate Answer
    response = retrieval_chain.invoke(
        {
            "input": question
        }
    )

    return response["answer"]