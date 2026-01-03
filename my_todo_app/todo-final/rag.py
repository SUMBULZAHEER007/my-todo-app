from typing import List, Dict, Any
from qdrant_client import QdrantClient
from langchain_qdrant import Qdrant
# Naya import path
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
import os
# Absolute import: 'models' file se 'TodoDB' class le rahe hain
import models
from sqlalchemy.orm import Session
from uuid import uuid4

class RAGService:
    """Service for Retrieval-Augmented Generation functionality"""

    def __init__(self):
        # Initialize Qdrant client
        qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if qdrant_api_key:
            self.client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        else:
            self.client = QdrantClient(url=qdrant_url)

        # Ensure your API key is set in environment variables
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.collection_name = "todos"
        self.vector_store = None

        # Create collection if it doesn't exist
        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            from qdrant_client.http import models as qdrant_models
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=qdrant_models.VectorParams(size=1536, distance=qdrant_models.Distance.COSINE),
            )

    def create_context_from_todos(self, db: Session, user_context: str = "") -> str:
        """Create context from existing todos for RAG"""
        # Fix: models.TodoDB use karein kyunki import 'models' hai
        todos = db.query(models.TodoDB).all()

        context_parts = []
        if user_context:
            context_parts.append(f"User context: {user_context}")

        if todos:
            context_parts.append("Current tasks:")
            for todo in todos:
                status = "completed" if todo.completed else "pending"
                context_parts.append(f"- ID {todo.id}: {todo.description} [{status}]")
        else:
            context_parts.append("No tasks currently in the system.")

        return "\n".join(context_parts)

    def build_vector_store(self, db: Session):
        """Build vector store from todos for similarity search"""
        todos = db.query(models.TodoDB).all()

        documents = []
        ids = []

        for todo in todos:
            content = f"Task ID: {todo.id}\nDescription: {todo.description}\nStatus: {'completed' if todo.completed else 'pending'}"
            doc = Document(
                page_content=content,
                metadata={"id": todo.id, "completed": todo.completed}
            )
            documents.append(doc)
            ids.append(str(uuid4()))

        if documents:
            self.vector_store = Qdrant.from_documents(
                documents=documents,
                embedding=self.embeddings,
                url=os.getenv("QDRANT_URL", "http://localhost:6333"),
                api_key=os.getenv("QDRANT_API_KEY"),
                collection_name=self.collection_name,
                ids=ids
            )

    def search_similar_tasks(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Search for similar tasks based on query"""
        if not self.vector_store:
            return []

        try:
            similar_docs = self.vector_store.similarity_search(query, k=k)
            results = []

            for doc in similar_docs:
                results.append({
                    "id": doc.metadata.get("id"),
                    "content": doc.page_content,
                    "completed": doc.metadata.get("completed")
                })

            return results
        except Exception as e:
            print(f"Error searching similar tasks: {e}")
            return []