import ollama


def ask_ollama(query, context):
    ### Envoie une question à Ollama en utilisant un contexte global
    prompt = f"""Voici les dernières actualités importantes :
    {context}
    En te basant sur ces informations, réponds à la question suivante : {query}
    📢 **Consignes :**  
    - Réponds comme une **journaliste** 📰.  
    - ** Ne dépasse pas 150 caractères** ⏳.  
    - ** Indique la date de chaque actualité, en priorisant celles du 6 février** 📅.  
    - ** SI tu sait pas dit je ne sait pas **.  
    """

    try:
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        return response.get("message", {}).get("content", "Aucune réponse reçue d'Ollama.")
    except Exception as e:
        return f"❌ Erreur Ollama : {str(e)}"


# Test manuel
if __name__ == "__main__":
    test_response = ask_ollama("Quels sont les derniers événements mondiaux ?", "Voici un contexte fictif.")
    print(f"🧠 Réponse d'Ollama : {test_response}")