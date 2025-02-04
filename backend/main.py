from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, Article
from ollama_handler import ask_ollama
from pydantic import BaseModel

app = FastAPI()

# Configuration CORS
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)