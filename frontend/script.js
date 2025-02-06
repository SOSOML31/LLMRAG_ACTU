function askQuestion() {
    const query = document.getElementById("query").value;
    const mode = document.getElementById("mode").value; // Récupération du mode sélectionné
    const endpoint = mode === "rag" ? "http://127.0.0.1:5000/ask" : "http://127.0.0.1:5000/llm";

    document.getElementById("response").innerText = "";
    document.getElementById("sources").innerHTML = "";
    document.getElementById("loading").style.display = "block"; // Affiche la barre de chargement

    fetch(endpoint, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("loading").style.display = "none"; // Cache la barre de chargement
        document.getElementById("response").innerText = data.response;

        if (mode === "rag" && data.sources) {
            const sourcesList = document.getElementById("sources");
            sourcesList.innerHTML = "";
            data.sources.forEach(source => {
                const li = document.createElement("li");
                li.innerHTML = `<a href="${source.url}" target="_blank">${source.title}</a>`;
                sourcesList.appendChild(li);
            });
        }
    })
    .catch(error => {
        document.getElementById("loading").style.display = "none"; // Cache la barre de chargement
        document.getElementById("response").innerText = "❌ Erreur lors de la requête.";
        console.error("Erreur:", error);
    });
}