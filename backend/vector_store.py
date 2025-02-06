import chromadb  # Importer ChromaDB pour la gestion des index vectoriels
from database import SessionLocal, Article  # Importer la connexion PostgreSQL et le modèle Article
from langchain_community.embeddings import HuggingFaceEmbeddings  # Importer le modèle d'embedding de LangChain

##############################################################################################################################################################################
##############################################################################################################################################################################
##############################################################################################################################################################################
#  Ce script crée un index vectoriel des articles dans ChromaDB à l’aide d’un modèle d’embeddings de LangChain.   ############################################################
##############################################################################################################################################################################
##############################################################################################################################################################################
##############################################################################################################################################################################
##############################################################################################################################################################################

# 1️⃣ **Initialisation de ChromaDB**
# ChromaDB est utilisé comme base de données vectorielle pour stocker et rechercher les articles sous forme d'embeddings.
chroma_client = chromadb.PersistentClient(path="chroma_db")  # Créer une base persistante pour stocker les embeddings des articles

# 2️⃣ **Définition du modèle d'embedding**
# Ce modèle convertit le texte en vecteurs pour permettre des recherches sémantiques efficaces.
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 3️⃣ **Création d'une collection ChromaDB**
# Une collection dans ChromaDB est similaire à une table en base de données. Elle contiendra les articles sous forme vectorisée.
collection = chroma_client.get_or_create_collection(name="articles")

# 4️⃣ **Fonction pour indexer les articles**
def index_articles():
    """
    - Récupère les articles stockés dans PostgreSQL.
    - Génère un embedding pour chaque article.
    - Ajoute l'article dans ChromaDB pour permettre une recherche rapide.
    """
    session = SessionLocal()  # Ouvrir une session pour interagir avec PostgreSQL
    articles = session.query(Article).all()  # Récupérer tous les articles de la base de données PostgreSQL

    for article in articles:
        # Générer un embedding du contenu de l'article
        embedding = embedding_function.embed_query(article.content)

        # Ajouter l'article et son embedding à la base vectorielle ChromaDB
        collection.add(
            ids=[str(article.id)],  # ID unique de l'article
            embeddings=[embedding],  # Embedding généré par le modèle
            documents=[article.content],  # Texte original de l'article
            metadatas=[{"title": article.title, "url": article.url}]  # Métadonnées (titre et lien)
        )

    session.close()  # Fermer la connexion à la base de données PostgreSQL
    print("✅ Articles indexés dans ChromaDB.")  # Message de confirmation

# 5️⃣ **Exécution du script**
if __name__ == "__main__":
    index_articles()  # Lancer l'indexation si le script est exécuté directement