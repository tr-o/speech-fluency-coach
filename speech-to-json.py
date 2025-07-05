import whisper
import json

filename = "data/data1.mp3"
model = whisper.load_model("base")
result = model.transcribe(filename)

# 保存
with open("data1_transcription.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("✅ Transcription saved to data1_transcription.json")