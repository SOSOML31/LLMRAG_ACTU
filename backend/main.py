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

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
def ask(request: QueryRequest):
    query = request.query

    session = SessionLocal()
    articles = session.query(Article).order_by(Article.created_at.desc()).limit(10).all()
    session.close()

    if not articles:
        raise HTTPException(status_code=404, detail="Aucun article trouvé.")

    # Correction ici - Assurer que la liste est bien formattée
    context = "\n\n".join([f"{article.title}: {article.content[:500]}..." for article in articles])

    sources = [{"title": article.title, "url": article.url} for article in articles]

    # Génération de la réponse avec Ollama
    response = ask_ollama(query, context)

    return {"response": response, "sources": sources}

@app.post("/llm")
def direct_llm_query(request: QueryRequest):
    """Appelle Ollama avec un modèle au choix"""
    query = request.query
    model = request.model if hasattr(request, "model") else "mistral"  # Mistral par défaut
    print(f"🧠 Requête LLM reçue : {query} | Modèle : {model}")

    # 🎯 Création du prompt simple
    prompt = f"Réponds de manière précise et détaillée à cette question : {query}"

    # 🤖 Envoi au LLM Ollama avec le modèle sélectionné
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])

    return {"response": response["message"]["content"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)