import feedparser
import requests
from bs4 import BeautifulSoup
from database import SessionLocal, Article

def fetch_rss_articles(rss_url):
    """Récupère les articles et les stocke dans PostgreSQL + ChromaDB."""
    session = SessionLocal()
    feed = feedparser.parse(rss_url)

    for entry in feed.entries:
        response = requests.get(entry.link)
        soup = BeautifulSoup(response.text, "html.parser")
        text = " ".join([p.text for p in soup.find_all("p")])

        # Vérifier si l'article existe déjà
        existing_article = session.query(Article).filter_by(url=entry.link).first()
        if not existing_article:
            new_article = Article(title=entry.title, url=entry.link, content=text)
            session.add(new_article)
            session.commit()
            print(f"✅ Article ajouté: {entry.title}")
        else:
            print(f"⚠️ Article déjà présent en base: {entry.title}")

    session.close()
    print("✅ Tous les articles ont été traités.")

fetch_rss_articles("https://www.france24.com/fr/rss")