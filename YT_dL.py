# liks.jsonにDLしたいyoutubeリンクを記載しておく。それらをまとめてダウンロードするプログラム。
import json

from yt_dlp import YoutubeDL

with open("download_list.json", "r") as f:
    data = json.load(f)
    links = data["urls"]  # JSON内でリンクが "urls" キーにあると仮定
ydl_opts = {
    "format": "bestvideo+bestaudio/best",
    "merge_output_format": "mkv",  # これを外せばmkv形式でDLされる
    "writeautomaticsub": True,
    "outtmpl": "../../Downloads/YLdownloads/%(title)s/%(title)s.%(ext)s",
    "subtitleslangs": ["en", "ja"],  # 必要に応じて言語を追加
}
yt_opts_instance = YoutubeDL(ydl_opts)

for link in links:
    yt_opts_instance.download([link])
