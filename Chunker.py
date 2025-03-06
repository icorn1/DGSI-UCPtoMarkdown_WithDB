import chromadb
import os
import html2text
from uuid import uuid4
from chromadb.utils import embedding_functions

# Crear conexión a ChromaDB (persistente)
chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection(name="web_scraper")

# Función para dividir texto en chunks
def split_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size)]

# Leer y procesar archivos Markdown
markdown_folder = "markdown_pages"

for filename in os.listdir(markdown_folder):
    filepath = os.path.join(markdown_folder, filename)
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    chunks = split_text(content)

    # Guardar cada chunk en ChromaDB
    for chunk in chunks:
        doc_id = str(uuid4())  # ID único
        collection.add(
            ids=[doc_id],
            documents=[chunk],
            metadatas=[{"source": filename}]
        )

print("✅ Archivos guardados en ChromaDB en chunks")
