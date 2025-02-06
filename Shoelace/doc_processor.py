import os
import markdown2
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb

DOCS_PATH = "docs/pages"  # 📂 Mets ici le chemin de la doc Shoelace
CHROMA_DB_PATH = "chroma_db"  # 📦 Stockage de la DB

# 🔥 Configuration du text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # Taille d'un chunk
    chunk_overlap=100  # Recouvrement pour garder du contexte
)

# 🔍 Initialisation de la base Chroma
chroma_client = chromadb.PersistentClient(CHROMA_DB_PATH)
collection = chroma_client.get_or_create_collection(name="shoelace_docs")


def process_markdown_docs():
    """Charge les fichiers markdown, les divise en chunks et les stocke."""
    for root, _, files in os.walk(DOCS_PATH):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)

                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    text = markdown2.markdown(content)  # Convertit Markdown en texte lisible

                    # 📝 Découpe en chunks
                    chunks = text_splitter.split_text(text)

                    # 📌 Ajoute chaque chunk à la DB vectorielle
                    for idx, chunk in enumerate(chunks):
                        collection.add(
                            documents=[chunk],
                            metadatas=[{"source": file, "chunk_id": idx}],
                            ids=[f"{file}_{idx}"]
                        )

    print("✅ Documentation indexée avec succès !")


if __name__ == "__main__":
    process_markdown_docs()