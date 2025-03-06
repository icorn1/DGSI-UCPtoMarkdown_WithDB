import chromadb
import os
import html2text
from uuid import uuid4
from sentence_transformers import SentenceTransformer

# Cargar modelo de embeddings (usa "all-MiniLM-L6-v2" por defecto)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Conectar a ChromaDB (persistente)
chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection(name="web_scraper")

# Función para dividir texto en chunks
def split_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size)]

# Leer archivos Markdown y generar embeddings
markdown_folder = "markdown_pages"

for filename in os.listdir(markdown_folder):
    filepath = os.path.join(markdown_folder, filename)
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    chunks = split_text(content)

    # Generar embeddings para cada chunk
    embeddings = model.encode(chunks).tolist()  # Convierte a listas para ChromaDB

    # Guardar en ChromaDB
    for chunk, embedding in zip(chunks, embeddings):
        doc_id = str(uuid4())  # ID único
        collection.add(
            ids=[doc_id],
            documents=[chunk],
            metadatas=[{"source": filename}],
            embeddings=[embedding]
        )

print("✅ Datos con embeddings almacenados en ChromaDB.")
