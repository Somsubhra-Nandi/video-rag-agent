import whisper
import os
import json

model = whisper.load_model("large-v2")

audios = os.listdir("audios")
os.makedirs("jsons", exist_ok=True)

for audio in audios:
    name, ext = os.path.splitext(audio)
    if "_" not in name:
        continue

    number, title = name.split("_", 1)
    number = number.replace(".mp4", "").strip()
    title = title.strip()

    print(number, title)

    result = model.transcribe(
        f"audios/{audio}",
        language="hi",
        task="translate",
        word_timestamps=False,
        fp16=False
    )

    chunks = []
    for segment in result["segments"]:
        chunks.append({
            "number": number,
            "title": title,
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"]
        })

    output = {
        "video_number": number,
        "video_title": title,
        "chunks": chunks,
        "full_text": result["text"]
    }

    with open(f"jsons/{number}.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
