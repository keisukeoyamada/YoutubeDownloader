# liks.jsonにDLしたいyoutubeリンクを記載しておく。それらをまとめてダウンロードするプログラム。
import json

from yt_dlp import YoutubeDL

with open("download_list.json", "r") as f:
    data = json.load(f)
    links = data["urls"]  # JSON内でリンクが "urls" キーにあると仮定

print("1: 動画をダウンロード\n2: 音声のみ（mp3）をダウンロード")
choice = input("番号を入力してください: ")

if choice == "1":
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mkv",  # これを外せばmkv形式でDLされる
        "writeautomaticsub": True,
        "outtmpl": "../../Downloads/YLdownloads/%(title)s/%(title)s.%(ext)s",
        "subtitleslangs": ["en", "ja"],  # 必要に応じて言語を追加
    }

if choice == "2":
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": "../../Downloads/YLdownloads/%(title)s/%(title)s.%(ext)s",
    }
else:
    print("1か2を選択してください。")
    exit()

yt_opts_instance = YoutubeDL(ydl_opts)

for link in links:
    yt_opts_instance.download([link])
