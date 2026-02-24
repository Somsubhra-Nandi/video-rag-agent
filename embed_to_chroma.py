import json
import os
import chromadb
import ollama
from tqdm import tqdm

# Where refined JSONs live
INPUT_DIR = "jsons_refined"

# Create / load vector DB
client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = client.get_or_create_collection(
    name="video_rag_bge_m3"
)

def embed_texts(texts):
    embeddings = []

    for text in texts:
        response = ollama.embeddings(
            model="bge-m3",
            prompt=text
        )
        embeddings.append(response["embedding"])

    return embeddings


documents = []
metadatas = []
ids = []

for file in os.listdir(INPUT_DIR):
    if not file.endswith(".json"):
        continue

    with open(os.path.join(INPUT_DIR, file), "r", encoding="utf-8") as f:
        data = json.load(f)

    for ch in data["chunks"]:
        documents.append(ch["text"])
        metadatas.append({
            "video_number": data["video_number"],
            "video_title": data["video_title"],
            "start": ch["start"],
            "end": ch["end"]
        })
        ids.append(ch["chunk_id"])

BATCH_SIZE = 32

for i in tqdm(range(0, len(documents), BATCH_SIZE)):
    batch_docs = documents[i:i+BATCH_SIZE]
    batch_meta = metadatas[i:i+BATCH_SIZE]
    batch_ids = ids[i:i+BATCH_SIZE]

    embeddings = embed_texts(batch_docs)

    collection.add(
        documents=batch_docs,
        metadatas=batch_meta,
        ids=batch_ids,
        embeddings=embeddings
    )

print("✅ Embeddings stored in Chroma")
