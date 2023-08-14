# 概要

アリスソフト「ドーナドーナ」の自作ジンザイ用の画像に変換するためのスクリプト。

# Big Respect

[【夏休み自由研究】実例で学ぶ画像処理【Python】 | 東京工業大学デジタル創作同好会 traP](https://trap.jp/post/1362/) by d_etteiu8383

# 準備

1. リポジトリを clone する

2. python3 をインストールする

3. poetry をインストールする

4. poetry を使ってパッケージをインストールする

```python
poetry install
```

5. カスケード型分類器（アニメ顔用）をダウンロードしてルートフォルダに設置する

[nagadomi/lbpcascade_animeface](https://github.com/nagadomi/lbpcascade_animeface)を使う。ファイル自体は[ここ](https://raw.githubusercontent.com/nagadomi/lbpcascade_animeface/master/lbpcascade_animeface.xml)

# 使い方

```python
poetry run python script.py
```
