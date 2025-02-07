from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, Article
from ollama_handler import ask_ollama
from pydantic import BaseModel
import ollama

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèle de requête attendu pour les endpoints POST
class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
def ask(request: QueryRequest):
    query = request.query  # Récupération de la requête utilisateur
    session = SessionLocal()  # Ouverture d'une session de base de données
    # Récupération des 10 articles les plus récents
    articles = session.query(Article).order_by(Article.created_at.desc()).limit(10).all()
    session.close()  # Fermeture de la session

    # Vérification si des articles sont disponibles
    if not articles:
        raise HTTPException(status_code=404, detail="Aucun article trouvé.")

    # Formatage du contexte à partir des articles récupérés
    context = "\n\n".join([f"{article.title}: {article.content[:500]}..." for article in articles])

    # Création d'une liste des sources pour la réponse
    sources = [{"title": article.title, "url": article.url} for article in articles]

    # Appel au modèle Ollama avec la requête et le contexte
    response = ask_ollama(query, context)

    return {"response": response, "sources": sources}  # Retourne la réponse du modèle et les sources utilisées


@app.post("/llm")
def direct_llm_query(request: QueryRequest):
    """Appelle directement Ollama avec un modèle au choix."""
    query = request.query  # Récupération de la requête utilisateur
    model = request.model if hasattr(request, "model") else "mistral"  # Sélection du modèle, Mistral par défaut

    print(f"🧠 Requête LLM reçue : {query} | Modèle : {model}")  # Log pour le suivi

    prompt = f"Réponds de manière précise et détaillée à cette question : {query}"

    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])

    return {"response": response["message"]["content"]}  # Retourne la réponse générée


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)