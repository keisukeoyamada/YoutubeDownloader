# liks.jsonにDLしたいyoutubeリンクを記載しておく。それらをまとめてダウンロードするプログラム。
import json
from yt_dlp import YoutubeDL

with open('download_list.json', 'r') as f:
    data = json.load(f)
    links = data['urls'] # JSON内でリンクが "urls" キーにあると仮定

yt_opts = YoutubeDL({'format':'mp4'})

for link in links:
    yt_opts.download([link])