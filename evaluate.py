import json
from rag_query import retrieve_evidence

def recall_at_k(eval_file, k=4):
    with open(eval_file, "r", encoding="utf-8") as f:
        eval_data = json.load(f)

    hits = 0

    for item in eval_data:
        question = item["question"]
        expected_video = item["expected_video"]

        evidences, _ = retrieve_evidence(question, k)

        retrieved_videos = {
            ev["video_number"] for ev in evidences
        }

        if expected_video in retrieved_videos:
            hits += 1

    recall = hits / len(eval_data)
    return recall


if __name__ == "__main__":
    score = recall_at_k("eval_questions.json", k=4)
    print(f"Recall@4: {score:.2f}")
