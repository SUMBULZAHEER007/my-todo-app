from typing import List, Dict, Any
from qdrant_client import QdrantClient
from langchain_qdrant import Qdrant
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import models
from sqlalchemy.orm import Session

class RAGService:
    def __init__(self):
        # Memory mode for quick setup
        self.client = QdrantClient(location=":memory:")
        self.collection_name = "todos"

        # Free Embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}  # Explicitly set device
        )
        self.vector_store = None

        # Collection setup
        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            from qdrant_client.http import models as qdrant_models
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=qdrant_models.VectorParams(size=384, distance=qdrant_models.Distance.COSINE),
            )

    def create_context_from_todos(self, db: Session, user_context: str = "") -> str:
        try:
            todos = db.query(models.TodoDB).all()
            context_parts = [f"User context: {user_context}"] if user_context else []
            if todos:
                context_parts.append("Current tasks in database:")
                for todo in todos:
                    status = "completed" if todo.completed else "pending"
                    context_parts.append(f"- ID {todo.id}: {todo.description} [{status}]")
            else:
                context_parts.append("The todo list is currently empty.")
            return "\n".join(context_parts)
        except Exception as e:
            print(f"Error creating context from todos: {str(e)}")
            return "Error retrieving tasks from database."

    def build_vector_store(self, db: Session):
        try:
            todos = db.query(models.TodoDB).all()
            documents = []
            for todo in todos:
                content = f"Task: {todo.description} (Status: {'Done' if todo.completed else 'Pending'})"
                documents.append(Document(
                    page_content=content,
                    metadata={"id": todo.id, "completed": todo.completed}
                ))

            if documents:
                # Updated to use Qdrant.from_documents with proper parameters
                self.vector_store = Qdrant.from_documents(
                    documents=documents,
                    embedding=self.embeddings,
                    location=":memory:",
                    collection_name=self.collection_name,
                    client=self.client
                )
        except Exception as e:
            print(f"Error building vector store: {str(e)}")
            self.vector_store = None

    def search_similar_tasks(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        try:
            if not self.vector_store:
                return []
            docs = self.vector_store.similarity_search(query, k=k)
            return [{"id": d.metadata["id"], "content": d.page_content, "completed": d.metadata["completed"]} for d in docs]
        except Exception as e:
            print(f"Error searching similar tasks: {str(e)}")
            return []