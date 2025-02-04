from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# Configuration de la base de données PostgreSQL
DB_URL = "postgresql://postgres:931752@localhost:5432/actullm"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    url = Column(String, unique=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# Création des tables
def create_tables():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables()
    print("✅ Base de données et tables créées avec succès.")