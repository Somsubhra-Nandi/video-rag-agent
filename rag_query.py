#importing required libraries

import chromadb
import ollama
import os
from dotenv import load_dotenv
from google import genai


#loading api key from .env file
load_dotenv()

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


#loading chroma db for retrieval layer
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("video_rag_bge_m3")

#embedding function for reusing ollama embeddings
def embed_query(text):
    response = ollama.embeddings(
        model="bge-m3",
        prompt=text
    )
    return response["embedding"]


#retrieval function
def retrieve_evidence(question, k=4):
    query_embedding = embed_query(question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )


    evidences = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        evidences.append({
            "video_number": meta["video_number"],
            "video_title": meta["video_title"],
            "start": meta["start"],
            "end": meta["end"],
            "text": doc
        })

    return evidences, results["distances"][0]


def distance_to_confidence(dist):
    if dist < 450:
        return "High"
    elif dist < 650:
        return "Medium"
    else:
        return "Low"


#creating prompt
def build_prompt(evidences, question):
    if not evidences:
        return None

    context = ""
    for i, ev in enumerate(evidences, 1):
        context += f"""
Source {i}:
Video {ev['video_number']} – {ev['video_title']}
Timestamp: {ev['start']}s to {ev['end']}s
Text: {ev['text']}
"""

    prompt = f"""
You are a factual question-answering system.

STRICT RULES:
- Answer in **ONE short paragraph**.
- Identify the **single most relevant source**.
- Do NOT list or explain multiple sources.
- If multiple sources mention similar things, choose the BEST one.
- Do NOT add commentary like "Source X states".
- End the answer with: (Video <number>, <start>s–<end>s)
- If the answer is not clearly present, say exactly:
  "Not found in the course content."

Sources:
{context}

Question:
{question}

Answer:
"""

    return prompt


#generation 

def generate_answer(prompt):
    response = gemini_client.models.generate_content(
        model="models/gemini-flash-lite-latest",
        contents=prompt
    )
    return response.text






# final answer loop
if __name__ == "__main__":
    while True:
        question = input("\nAsk a question (or type 'exit'): ")

        if question.lower() == "exit":
            break

        evidences, distances = retrieve_evidence(question)

        prompt = build_prompt(evidences, question)
        if prompt is None:
            print("Not found in the course content.")
            continue

        answer = generate_answer(prompt)
        print("\nANSWER:\n", answer)
        if answer.strip() == "Not found in the course content.":
            continue
        
        print("\nEVIDENCE:")
        for ev in evidences:
            print(
                f"- Video {ev['video_number']} "
                f"[{ev['start']}s–{ev['end']}s]"
            )

        # ✅ MOVE CONFIDENCE HERE
        top_distance = distances[0]
        confidence = distance_to_confidence(top_distance)
        print(f"Distance: {top_distance}")
        print(f"\nConfidence: {confidence}")

