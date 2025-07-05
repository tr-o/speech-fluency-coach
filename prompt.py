import json

# Whisperの出力ファイルを読み込み
with open("data1_transcription.json", "r", encoding="utf-8") as f:
    result = json.load(f)

# セグメントをすべて結合
full_script = " ".join([seg["text"].strip() for seg in result["segments"]])

# Markdown用プロンプト
prompt_md = """
# 🧠 Prompt for AI Analysis

Please analyze the following English speech. It was spoken spontaneously by a non-native speaker who is practicing fluency. Your tasks are:

1. Go through the script sentence by sentence.
2. For each sentence:
   - If the sentence is grammatically correct and natural, say: ✅ "This sentence is natural and fluent."
   - If the sentence is grammatically incorrect, awkward, or unclear, say: ❌ "This sentence needs improvement." Then:
     - Identify what the speaker was trying to say.
     - Suggest a clearer and more appropriate version.
     - Explain your reasoning for the change.
3. After analyzing all sentences, rewrite the entire script into natural, fluent English.

Be constructive and supportive, as if you are an English speaking coach. Focus on clarity, fluency, and confidence-building.
"""

# Markdownファイルに書き出し
with open("ai_analysis_input.md", "w", encoding="utf-8") as f:
    f.write("# 📝 Transcribed Script\n\n")
    f.write(full_script.strip() + "\n\n")
    f.write("---\n\n")
    f.write(prompt_md.strip())

print("✅ Markdownファイル 'ai_analysis_input.md' を生成しました。")