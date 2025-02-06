from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb
import ollama

# 📂 Initialise la DB Chroma
chroma_client = chromadb.PersistentClient("chroma_db")
collection = chroma_client.get_collection(name="shoelace_docs")

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
def ask(request: QueryRequest):
    query = request.query

    print(f"🧐 Requête reçue : {query}")

    # 🔎 Recherche dans la base vectorielle
    results = collection.query(query_texts=[query], n_results=3)

    # 📌 Vérification si on a trouvé des documents
    if not results["documents"]:
        raise HTTPException(status_code=404, detail="Aucune information trouvée.")

    # 📝 Construire le contexte avec les passages récupérés
    context = "\n\n".join([f"{doc['metadata']['source']}: {doc['documents']}" for doc in results["documents"]])

    # 🎯 Création du prompt pour Ollama
    prompt = f"""Voici des extraits de la documentation Shoelace :
    {context}

    Répondez à la question : {query}"""

    # 🤖 Envoi à Ollama
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])

    return {"response": response["message"]["content"], "sources": results["metadatas"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)