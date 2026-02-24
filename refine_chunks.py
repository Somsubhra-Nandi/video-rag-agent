import json
import os

INPUT_DIR = "jsons"
OUTPUT_DIR = "jsons_refined"
MAX_CHARS = 800

os.makedirs(OUTPUT_DIR, exist_ok=True)

def merge_chunks(chunks, max_chars=MAX_CHARS):
    merged = []
    buffer = []
    char_count = 0

    for ch in chunks:
        text = ch["text"].strip()
        length = len(text)

        if char_count + length > max_chars and buffer:
            merged.append({
                "start": buffer[0]["start"],
                "end": buffer[-1]["end"],
                "text": " ".join(b["text"].strip() for b in buffer)
            })
            buffer = []
            char_count = 0

        buffer.append(ch)
        char_count += length

    if buffer:
        merged.append({
            "start": buffer[0]["start"],
            "end": buffer[-1]["end"],
            "text": " ".join(b["text"].strip() for b in buffer)
        })

    return merged

for file in os.listdir(INPUT_DIR):
    if not file.endswith(".json"):
        continue

    with open(os.path.join(INPUT_DIR, file), "r", encoding="utf-8") as f:
        data = json.load(f)

    merged_chunks = merge_chunks(data["chunks"])

    refined = []
    for i, ch in enumerate(merged_chunks):
        video_number = data["chunks"][0]["number"]
        video_title = data["chunks"][0]["title"]
        refined.append({
            "chunk_id": f"{video_number}_{i}",
            "video_number": video_number,
            "video_title": video_title,
            "start": ch["start"],
            "end": ch["end"],
            "duration": ch["end"] - ch["start"],
            "text": ch["text"],
            "char_len": len(ch["text"])
        })

    out = {
        "video_number": video_number,
        "video_title": video_title,
        "chunks": refined
    }


    with open(os.path.join(OUTPUT_DIR, file), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

print("Refinement done")
