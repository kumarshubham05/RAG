from dotenv import load_dotenv
import os
import re

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

    # -----------------------------
    # Load documents
    # -----------------------------
    loader = DirectoryLoader(
        path=os.path.join(BASE_DIR, "infra_docs"),
        glob="**/*.md",
        loader_cls=lambda path: TextLoader(path, encoding="utf-8")
    )

    documents = loader.load()
    if not documents:
        raise RuntimeError("No infra documents found")

    # -----------------------------
    # Chunk documents
    # -----------------------------
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = text_splitter.split_documents(documents)

    # -----------------------------
    # Add metadata (incident_id, date, type)
    # -----------------------------
    for chunk in chunks:
        chunk.metadata["type"] = "general"

        inc_match = re.search(r"INC-\d+", chunk.page_content)
        if inc_match:
            chunk.metadata["incident_id"] = inc_match.group()
            chunk.metadata["type"] = "incident"

        date_match = re.search(r"\b\d{2}-[A-Za-z]{3}-\d{4}\b", chunk.page_content)
        if date_match:
            chunk.metadata["incident_date"] = date_match.group()

    # -----------------------------
    # Vector store
    # -----------------------------
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_db = FAISS.from_documents(chunks, embeddings)

    # -----------------------------
    # Dynamic retriever (ID + Date aware)
    # -----------------------------
    def get_retriever(question: str):
        inc_match = re.search(r"INC-\d+", question)
        date_match = re.search(r"\b\d{2}-[A-Za-z]{3}-\d{4}\b", question)

        filters = {}

        if inc_match:
            filters["incident_id"] = inc_match.group()

        if date_match:
            filters["incident_date"] = date_match.group()

        if filters:
            return vector_db.as_retriever(
                search_kwargs={
                    "k": 10,
                    "filter": filters
                }
            )

        # Default for FAQs / architecture / processes
        return vector_db.as_retriever(search_kwargs={"k": 3})

    # -----------------------------
    # LLM
    # -----------------------------
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are an internal DevOps assistant.
Answer ONLY from the context.
If the answer is not present, say:
"I don't have information about that."

Context:
{context}

Question:
{question}

Answer:
"""
    )

    # -----------------------------
    # QA function (callable)
    # -----------------------------
    def qa(query: str):
        retriever = get_retriever(query)

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True
        )

        return qa_chain.invoke({"query": query})

    return qa
