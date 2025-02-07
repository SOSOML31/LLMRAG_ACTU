import ollama
def ask_ollama(query, context):
    ### Envoie une question à Ollama en utilisant un contexte global
    prompt = f"""Voici les dernières actualités importantes :
    {context}
    En te basant sur ces informations, réponds à la question suivante : {query}
    📢 **Consigns :**  
    - Réponds comme une **journaliste** 📰.  
    - ** Ne dépasse pas 150 caractères** ⏳.  
    - ** Indique la date de chaque actualité, en priorisant celles du 6 février** 📅.  
    - ** Si tu comprend pas ou que tu as pas de sujet direct avec la question {query} dit vous pouvez reformuler**.  
    """
    try:
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        return response.get("message", {}).get("content", "Aucune réponse reçue d'Ollama.")
    except Exception as e:
        return f"❌ Erreur Ollama : {str(e)}"

if __name__ == "__main__":
    test_response = ask_ollama("Quels sont les derniers événements mondiaux ?", "Voici un contexte fictif.")
    print(f"🧠 Réponse d'Ollama : {test_response}")