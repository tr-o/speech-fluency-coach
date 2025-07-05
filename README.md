# python-speaking-learning-helper

## 🎯 プロジェクト概要

本プロジェクトは、英語スピーキング力の向上を目的とした自己記録・分析ツールである。録音された英語音声（5〜15分程度）を文字起こしし、話者の発話傾向や課題を定量的に可視化することで、継続的な改善と学習モチベーションの維持を支援する。

---

## 🔧 実装予定機能

### 1. 📊 発話速度の計測（Words per Minute）

- **目的**：話すスピードの変化を定量的に把握する
- **機能内容**：
  - 音声全体に対する平均発話速度（WPM: Words per Minute）を算出
  - 1分ごとのWPMを時系列で出力（例：グラフや表形式）

### 2. 🧾 文の長さの統計分析

- **目的**：話者がどれだけ長く・まとまった文を話せているかを評価
- **機能内容**：
  - 1文あたりの単語数の平均・中央値・最大値・最小値を算出
  - 文の分割はピリオドや明確なポーズ（Whisperのセグメント）を基準とする

### 3. ⏸️ 言い淀みの検出と指標化

- **目的**：流暢さの課題を可視化し、改善のヒントを得る
- **機能内容**：
  - 以下のような言い淀み表現の出現頻度をカウント：
    - 繰り返し（例：I... I don't know）
    - フィラー（例：uh, um, like, well, okay, whatever）
    - 言い直し（例：expect... except... except for）
  - 全体の単語数に対する言い淀みの割合（%）を算出

---

## 📁 出力形式（予定）

- テキストファイル（.txt）またはMarkdown（.md）で保存
- 統計情報と文字起こし本文を併記
- オプションでグラフ（matplotlibなど）による可視化も対応

---

## 🧩 拡張予定（将来的なアイデア）

- AIによる自然な英語へのリライト
- 間違い・不自然な表現のフィードバック
- スピーキング成長の時系列比較（過去ログとの比較）

## 環境構築
- whisperのinstall
    - pip install git+https://github.com/openai/whisper.git
    - https://qiita.com/taiki_i/items/99cb17049597fdee6ce2
- ffmegのinstall
    - バイナリダウンロード：https://github.com/BtbN/FFmpeg-Builds/releases
    - 環境変数に追加：C:\Program Files\ffmpeg-master-latest-win64-gpl-shared\bin
