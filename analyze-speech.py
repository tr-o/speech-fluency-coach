import json
from collections import defaultdict

# 色パレット（15分まで対応）
colors = [
    "#e0f7fa", "#e8f5e9", "#fff9c4", "#f3e5f5", "#e3f2fd",
    "#ffebee", "#f1f8e9", "#fff3e0", "#fce4ec", "#ede7f6",
    "#fbe9e7", "#e0f2f1", "#f9fbe7", "#f5f5f5", "#edeef0"
]

# JSON読み込み
with open("data1_transcription.json", "r", encoding="utf-8") as f:
    result = json.load(f)

segments = result["segments"]

# セグメントを1分ごとに分類
minute_segments = defaultdict(list)
for i, segment in enumerate(segments):
    minute = int(segment["start"] // 60)
    minute_segments[minute].append((i + 1, segment["text"].strip()))

# HTML構築
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Transcription by Minute</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }
        .minute-block { padding: 10px; margin-bottom: 10px; border-radius: 8px; }
        .segment { margin-left: 1em; }
        .minute-title { font-weight: bold; margin-bottom: 5px; }
    </style>
</head>
<body>
<h1>📝 Transcription Segmented by Minute</h1>
"""

for minute in sorted(minute_segments):
    color = colors[minute % len(colors)]
    html += f'<div class="minute-block" style="background-color: {color};">\n'
    html += f'<div class="minute-title">⏱️ Minute {minute:02d}:00 - {minute+1:02d}:00</div>\n'
    for idx, text in minute_segments[minute]:
        html += f'<div class="segment">[{idx:03d}] {text}</div>\n'
    html += '</div>\n'

html += "</body></html>"

# 保存
with open("transcription_by_minute.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ HTML file saved as 'transcription_by_minute.html'")