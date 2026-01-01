from dotenv import load_dotenv
import os

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA


def build_qa_chain():
    load_dotenv()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    loader = DirectoryLoader(
        path=os.path.join(BASE_DIR, "infra_docs"),
        glob="**/*.md",
        loader_cls=lambda path: TextLoader(path, encoding="utf-8")
    )

    documents = loader.load()
    if not documents:
        raise RuntimeError("No infra documents found")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_db = FAISS.from_documents(chunks, embeddings)

    retriever = vector_db.as_retriever(
        search_kwargs={"k": 1}
    )

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are an internal DevOps assistant.
Answer ONLY from the context.
If not found, say "I don't have information about that."

Context:
{context}

Question:
{question}

Answer:
"""
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )

