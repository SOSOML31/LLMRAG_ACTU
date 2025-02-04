import chromadb
from database import SessionLocal, Article
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# Initialiser ChromaDB
chroma_client = chromadb.PersistentClient(path="chroma_db")

# Embedding model (compatible avec Ollama)
embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Création de l'index
collection = chroma_client.get_or_create_collection(
    name="articles", embedding_function=embedding_function
)


# Ajouter les articles à l'index
def index_articles():
    session = SessionLocal()
    articles = session.query(Article).all()

    for article in articles:
        collection.add(
            ids=[str(article.id)],
            documents=[article.content],
            metadatas=[{"title": article.title, "url": article.url}]
        )

    session.close()
    print("✅ Articles indexés dans ChromaDB.")


if __name__ == "__main__":
    index_articles()