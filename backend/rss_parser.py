import feedparser
import requests
from bs4 import BeautifulSoup
from database import SessionLocal, Article
##############################################################################################################################################################################
##############################################################################################################################################################################
##############################################################################################################################################################################
#        🎯 Ce script récupère des articles depuis un flux RSS et les stocke dans PostgreSQL et ChromaDB.                         ###########################################
##############################################################################################################################################################################
##############################################################################################################################################################################
##############################################################################################################################################################################
##############################################################################################################################################################################

def fetch_rss_articles(rss_url):
    """
    📌 Cette fonction :
    1️⃣ Télécharge le flux RSS depuis une URL donnée.
    2️⃣ Extrait le contenu des articles en HTML et le convertit en texte.
    3️⃣ Vérifie si l'article existe déjà en base de données (PostgreSQL).
    4️⃣ Si l'article est nouveau, il est ajouté à PostgreSQL.
    """
    session = SessionLocal()
    feed = feedparser.parse(rss_url)

    for entry in feed.entries:  # Boucle sur chaque article du flux RSS

        # Récupérer le contenu de l'article via son lien
        response = requests.get(entry.link)
        soup = BeautifulSoup(response.text, "html.parser")  # Parser le HTML de l'article

        # Extraire le texte des balises <p> pour obtenir uniquement le contenu
        text = " ".join([p.text for p in soup.find_all("p")])

        # Vérifier si l'article est déjà en base (on vérifie via l'URL unique)
        existing_article = session.query(Article).filter_by(url=entry.link).first()

        if not existing_article:  # Si l'article n'est PAS encore dans la base
            # 4️⃣ Créer un nouvel objet Article pour le stocker dans PostgreSQL
            new_article = Article(title=entry.title, url=entry.link, content=text)
            session.add(new_article)  # Ajouter l'article à la session SQL
            session.commit()  # Enregistrer dans la base
            print(f"✅ Article ajouté: {entry.title}")  # Affichage en console
        else:
            print(f"⚠️ Article déjà présent en base: {entry.title}")  # Détection des doublons

    session.close()  # Fermer la connexion PostgreSQL
    print("✅ Tous les articles ont été traités.")  # Indiquer la fin du processus

fetch_rss_articles("https://www.france24.com/fr/rss")