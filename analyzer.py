import json
import statistics
from collections import defaultdict
import matplotlib.pyplot as plt
import io
import base64

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

# 分ごとのセグメントと統計用データ
minute_segments = defaultdict(list)
minute_word_counts = defaultdict(float)
minute_sentence_lengths = defaultdict(list)
total_words = 0
sentence_lengths = []

# 言い淀み検出用
filler_words = {"uh", "um", "like", "well", "okay", "so", "hmm", "you know", "i mean"}
filler_count = 0
repetition_count = 0

# 分類処理
for i, segment in enumerate(segments):
    start = segment["start"]
    end = segment["end"]
    minute = int(start // 60)
    text = segment["text"].strip()
    words = text.split()
    word_count = len(words)

    if word_count == 0:
        continue

    # セグメント保存
    minute_segments[minute].append((i + 1, text, word_count))
    minute_word_counts[minute] += word_count
    minute_sentence_lengths[minute].append(word_count)
    sentence_lengths.append(word_count)
    total_words += word_count

    # 言い淀み検出
    lower_words = [w.strip(".,!?").lower() for w in words]
    for j in range(len(lower_words)):
        if lower_words[j] in filler_words:
            filler_count += 1
        if j > 0 and lower_words[j] == lower_words[j - 1]:
            repetition_count += 1

# 全体統計
total_duration_sec = segments[-1]["end"]
total_minutes = total_duration_sec / 60
average_wpm = total_words / total_minutes
wpm_values = list(minute_word_counts.values())

# HTML構築
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Transcription Report</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }
        .minute-block { padding: 10px; margin-bottom: 10px; border-radius: 8px; }
        .segment { margin-left: 1em; }
        .minute-title { font-weight: bold; margin-bottom: 5px; }
        .summary { margin-top: 40px; padding: 15px; background-color: #f0f0f0; border-radius: 8px; }
        .summary h2 { margin-top: 0; }
        img { max-width: 100%; height: auto; }
    </style>
</head>
<body>
<h1>📝 Transcription Report</h1>
"""

# 各分のセクション
for minute in sorted(minute_segments):
    color = colors[minute % len(colors)]
    wpm = minute_word_counts[minute]
    avg_len = statistics.mean(minute_sentence_lengths[minute])
    html += f'<div class="minute-block" style="background-color: {color};">\n'
    html += f'<div class="minute-title">⏱️ Minute {minute:02d}:00 - {minute+1:02d}:00 | WPM: {wpm:.1f} | Avg Sentence Length: {avg_len:.1f} words</div>\n'
    for idx, text, count in minute_segments[minute]:
        html += f'<div class="segment">[{idx:03d}] {text}</div>\n'
    html += '</div>\n'

# 統計サマリー
filler_ratio = filler_count / total_words * 100
repetition_ratio = repetition_count / total_words * 100

html += """
<div class="summary">
<h2>📊 Summary Statistics</h2>
<ul>
"""
html += f"<li><strong>Average WPM:</strong> {average_wpm:.2f}</li>\n"
html += f"<li><strong>WPM Range:</strong> {min(wpm_values):.1f} - {max(wpm_values):.1f}</li>\n"
html += f"<li><strong>Total Sentences:</strong> {len(sentence_lengths)}</li>\n"
html += f"<li><strong>Average Sentence Length:</strong> {statistics.mean(sentence_lengths):.2f} words</li>\n"
html += f"<li><strong>Median Sentence Length:</strong> {statistics.median(sentence_lengths):.2f} words</li>\n"
html += f"<li><strong>Sentence Length Range:</strong> {min(sentence_lengths)} - {max(sentence_lengths)} words</li>\n"
html += f"<li><strong>Filler Words:</strong> {filler_count} ({filler_ratio:.2f}%)</li>\n"
html += f"<li><strong>Repetitions:</strong> {repetition_count} ({repetition_ratio:.2f}%)</li>\n"
html += "</ul>\n</div>\n"

# グラフ生成関数
def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

# WPMグラフ
fig1, ax1 = plt.subplots(figsize=(8, 3))
minutes = sorted(minute_word_counts.keys())
wpm_vals = [minute_word_counts[m] for m in minutes]
ax1.plot(minutes, wpm_vals, marker='o', color='blue')
ax1.axhline(y=average_wpm, color='red', linestyle='--', label=f'Avg: {average_wpm:.1f}')
ax1.set_title("Words Per Minute Over Time")
ax1.set_xlabel("Minute")
ax1.set_ylabel("WPM")
ax1.grid(True)
ax1.legend()
wpm_base64 = fig_to_base64(fig1)
plt.close(fig1)

# 文長ヒストグラム
fig2, ax2 = plt.subplots(figsize=(8, 3))
ax2.hist(sentence_lengths, bins=range(0, max(sentence_lengths)+5, 2), color='green', edgecolor='black')
ax2.set_title("Sentence Length Distribution")
ax2.set_xlabel("Words per Sentence")
ax2.set_ylabel("Frequency")
ax2.grid(True)
hist_base64 = fig_to_base64(fig2)
plt.close(fig2)

# HTMLにグラフ追加
html += f"""
<div class="summary">
<h2>📉 Visual Summary</h2>
<h3>WPM Over Time</h3>
<img src="data:image/png;base64,{wpm_base64}" alt="WPM Graph"><br>
<h3>Sentence Length Distribution</h3>
<img src="data:image/png;base64,{hist_base64}" alt="Sentence Length Histogram">
</div>
"""

html += "</body></html>"

# 保存
with open("transcription_report.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ HTML report saved as 'transcription_report.html'")