import whisper
import math
from collections import defaultdict
import matplotlib.pyplot as plt
import japanize_matplotlib  # 日本語表示が必要な場合

# ファイルとモデル
filename = "data/data1.mp3"
model = whisper.load_model("base")
result = model.transcribe(filename)

# 全文の表示
print("📝 文字起こし全文:\n")
full_text = result["text"]
print(full_text)

# セグメントごとの単語数を1分単位で集計
minute_bins = defaultdict(int)
total_words = 0

for segment in result["segments"]:
    start_minute = int(segment["start"] // 60)
    words = segment["text"].strip().split()
    word_count = len(words)
    minute_bins[start_minute] += word_count
    total_words += word_count

# 音声全体の長さ（分）
total_duration_sec = result["segments"][-1]["end"]
total_minutes = total_duration_sec / 60
average_wpm = total_words / total_minutes

# 結果表示
print(f"\n🎯 平均WPM（全体）: {average_wpm:.2f}")
print("📊 各分ごとのWPM:")
for minute in sorted(minute_bins):
    print(f"  {minute:02d}分目: {minute_bins[minute]} words")

# グラフ描画
minutes = sorted(minute_bins.keys())
wpm_values = [minute_bins[m] for m in minutes]

plt.figure(figsize=(10, 5))
plt.plot(minutes, wpm_values, marker='o', linestyle='-', color='blue', label='WPM')
plt.axhline(y=average_wpm, color='red', linestyle='--', label=f'平均WPM: {average_wpm:.1f}')
plt.title("1分ごとの発話速度（WPM）")
plt.xlabel("分")
plt.ylabel("単語数（Words per Minute）")
plt.xticks(minutes)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()