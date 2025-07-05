import whisper

filename = "data/data1.mp3"
model = whisper.load_model("base")
result = model.transcribe(filename)
print("result:")
print(result["text"])