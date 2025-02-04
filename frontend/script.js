function askQuestion() {
    const query = document.getElementById("query").value;

    fetch("http://127.0.0.1:5000/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("response").innerText = data.response;
        const sourcesList = document.getElementById("sources");
        sourcesList.innerHTML = "";
        data.sources.forEach(source => {
            const li = document.createElement("li");
            li.innerHTML = `<a href="${source.url}" target="_blank">${source.title}</a>`;
            sourcesList.appendChild(li);
        });
    });
}