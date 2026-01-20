"""
Simple RAG (Retrieval Augmented Generation) system using Google Gemini.
Reads a text file, creates embeddings, and answers questions using context.
"""
import os
import pymupdf
from pathlib import Path

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.messages import HumanMessage
from langchain_core.documents import Document

from config import local, keywords, questions, parameters, paths
from src import data_loading

class ArchiChat:
    """Gemini RAG based on with a pdf of construction law of stated in Poland."""

    def __init__(self, api_key: str, vectorstore_path: str = "./vectorstore"):
        """
        Initialize the RAG system.

        Args:
            api_key: Google API key
            vectorstore_path: Path to save/load the vector store
        """
        self.api_key = api_key
        self.vectorstore_path = vectorstore_path

        # Initialize embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=parameters.EMBEDDING_MODEL,
            api_key=api_key
        )

        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model=parameters.LLM_MODEL,
            api_key=api_key,
            temperature=parameters.LLM_TEMPERATURE
        )

        self.vectorstore = None

    def load_and_index_document(self, file_path: str, chunk_size: int = 200, chunk_overlap: int = 20):
        """
        Load a text file and create vector store.

        Args:
            file_path: Path to the text file
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        print("Loading document...")

        documents = data_loading.load_context_file(file_path)

        print("Splitting text into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            keep_separator=True,
            separators=[keywords.CHAPTER_PATTERN, keywords.ART_PATTERN],
            # separators=[keywords.CHAPTER_PATTERN, keywords.ART_PATTERN, keywords.ARTICLE_POINT_PATTERN],
            is_separator_regex=True
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Created {len(chunks)} chunks")

        print("Creating embeddings and vector store...")
        self.vectorstore = FAISS.from_documents(chunks, self.embeddings)

        print("Saving vector store locally...")
        self.save_vectorstore()
        print(f"Vector store saved to {self.vectorstore_path}")


    def save_vectorstore(self):
        """Save the vector store to disk."""
        if self.vectorstore:
            self.vectorstore.save_local(self.vectorstore_path)

    def load_vectorstore(self):
        """Load the vector store from disk."""
        if os.path.exists(self.vectorstore_path):
            print(f"Loading vector store from {self.vectorstore_path}...")
            self.vectorstore = FAISS.load_local(
                self.vectorstore_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            print("Vector store loaded successfully!")
        else:
            print(f"No vector store found at {self.vectorstore_path}")

    def search_and_answer(self, query: str, top_k: int = 1) -> str:
        """
        Search for relevant documents and generate an answer.

        Args:
            query: User's question
            top_k: Number of relevant chunks to retrieve

        Returns:
            Generated answer
        """
        if not self.vectorstore:
            return "Vector store not initialized. Please load or create one first."

        # Search for relevant documents
        results = self.vectorstore.similarity_search(query, k=top_k)

        # Extract text from results
        texts = [doc.page_content for doc in results]
        context = "\n\n".join(texts)

        print(f"The found context are {top_k} chunks:\n")
        for chunk_idx, chunk in enumerate(texts):
            print(f"{chunk_idx+1}. {chunk}")

        if not context:
            return "No relevant documents found."

        prompt = f"""Odpowiedz na poniższe pytanie na podstawie mając jako kontekst poniższy fragment prawa budowlanego.

        Pytanie: {query}

        Fragment prawa:
        {context}

        Odpowiedź:"""

        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content


# Main execution
if __name__ == "__main__":
    # Configuration
    context_filepath = paths.CONTEXT_FILEPATH
    vectorstore_dir_name = f"{Path(context_filepath).stem}_{parameters.EMBEDDING_MODEL}_chunk_size{parameters.CHUNK_SIZE}_overlap{parameters.CHUNK_OVERLAP}"
    VECTORSTORE_PATH = os.path.join(paths.VECTORSTORE_DIR, vectorstore_dir_name)

    # Initialize RAG system
    rag = ArchiChat(api_key=local.GENAI_API_KEY, vectorstore_path=VECTORSTORE_PATH)

    # Check if vector store exists, otherwise create it
    if os.path.exists(VECTORSTORE_PATH):
        rag.load_vectorstore()
    else:
        print("Creating new vector store...")
        rag.load_and_index_document(context_filepath, parameters.CHUNK_SIZE, parameters.CHUNK_OVERLAP)

    question = questions.art_45b_question_yes_no_1
    answer = rag.search_and_answer(question, top_k=parameters.NUM_CONTEXT_CHUNKS)

    print(f"Pytanie: {question}")
    print(f"\nOdpowiedź: {answer}")
