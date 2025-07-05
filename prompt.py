import json

# Whisperの出力ファイルを読み込み
with open("data1_transcription.json", "r", encoding="utf-8") as f:
    result = json.load(f)

segments = result["segments"]

# セグメントを番号付きでMarkdown化
segment_lines = []
for i, seg in enumerate(segments):
    text = seg["text"].strip()
    if text:
        segment_lines.append(f"[Segment {i+1:03d}] {text}")

# 改訂プロンプト（文法的に厳密＋出力簡潔化）
prompt_md = """
# 🧠 Prompt for AI Analysis

Please analyze the following English speech, which was spoken spontaneously by a non-native speaker practicing fluency. The script is divided into numbered segments.

Your tasks are:

1. Go through each segment by its number.
2. If a segment is extremely short (e.g., only one or two words), and it is clearly part of a longer idea, feel free to mentally combine it with adjacent segments for better interpretation.
   - If you do combine segments, clearly indicate which segment numbers were merged in your response (e.g., "[Segments 162–165] were interpreted together").
3. For each segment (or combined idea):
   - If the sentence is grammatically correct, idiomatic, and natural-sounding in standard English, list the segment number under a ✅ Natural and Fluent Segments section.
   - If the sentence contains grammatical errors, awkward phrasing, unnatural word order, or redundancy, list it under a ❌ Needs Improvement section and provide:
     - A clearer and more appropriate version (1 sentence)
     - A brief reason for the change (1 sentence)
   - Do not repeat the original sentence. Refer to it only by its segment number.

⚠️ Be strict in your judgment. Do not mark a sentence as ✅ just because it is understandable. Only mark it as ✅ if it would be considered correct and natural by a native English speaker in everyday conversation or writing.

Focus on grammar, word choice, and sentence structure. You do not need to analyze hesitations or disfluencies.  
Be constructive and supportive, as if you are an English speaking coach.
"""

# Markdownファイルに書き出し
with open("ai_analysis_input.md", "w", encoding="utf-8") as f:
    f.write("# 📝 Transcribed Segments\n\n")
    f.write("\n".join(segment_lines))
    f.write("\n\n---\n\n")
    f.write(prompt_md.strip())

print("✅ Markdownファイル 'ai_analysis_input.md' を生成しました。")