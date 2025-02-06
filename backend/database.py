from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime  # Import des types de colonnes SQL
from sqlalchemy.orm import sessionmaker, declarative_base  # ORM pour gérer la base
from datetime import datetime  # Gestion des dates et heures

##############################################################################################################################################################################
##############################################################################################################################################################################
##############################################################################################################################################################################
#  🎯 Ce script configure la connexion à PostgreSQL et définit la structure de la table "articles".         #################################################################
##############################################################################################################################################################################
##############################################################################################################################################################################
##############################################################################################################################################################################

# 📌 1️⃣ Configuration de la connexion à PostgreSQL
DB_URL = "postgresql://postgres:931752@localhost:5432/actullm"  # ⚠️ Remplace par tes propres identifiants
engine = create_engine(DB_URL)  # Création du moteur de connexion SQLAlchemy
# 📌 2️⃣ Création de la session pour interagir avec la base de données
SessionLocal = sessionmaker(bind=engine)  # Génère des sessions pour interagir avec la base
# 📌 3️⃣ Définition de la classe de base pour les modèles SQLAlchemy
Base = declarative_base()  # Classe de base pour les modèles ORM
# 📌 4️⃣ Définition du modèle de la table "articles"
class Article(Base):
    """
    🎯 Modèle SQLAlchemy représentant un article stocké dans la base de données.
    """
    __tablename__ = "articles"  # Nom de la table dans PostgreSQL

    id = Column(Integer, primary_key=True, index=True)  # ID unique auto-incrémenté
    title = Column(String, index=True)  # Titre de l'article (indexé pour les recherches)
    url = Column(String, unique=True, index=True)  # URL de l'article (doit être unique)
    content = Column(Text)  # Contenu texte de l'article
    created_at = Column(DateTime, default=datetime.utcnow)  # Date de création (automatique)

# 📌 5️⃣ Fonction pour créer les tables dans la base de données
def create_tables():
    """
        Cette fonction crée la table "articles" dans la base de données si elle n'existe pas.
    """
    Base.metadata.create_all(engine)  # Créer les tables basées sur les modèles définis

# 📌 6️⃣ Lancer la création de la base de données
if __name__ == "__main__":
    create_tables()  # Appel de la fonction pour créer les tables
    print("✅ Base de données et tables créées avec succès.")  # Message de confirmation