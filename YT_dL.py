# liks.jsonにDLしたいyoutubeリンクを記載しておく。それらをまとめてダウンロードするプログラム。
import json

from yt_dlp import YoutubeDL

import GetListfromYT_Auth as GetList

with open("download_list.json", "r") as f:
    data = json.load(f)
    links = data["urls"]  # JSON内でリンクが "urls" キーにあると仮定

while True:
    print("1: 動画をダウンロード\n2: 音声のみ（mp3）をダウンロード\n3: DLリストを確認\n4: 終了")
    choice = input("番号を入力してください: ")

    if choice == "1":
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

    elif choice == "2":
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
        yt_opts_instance = YoutubeDL(ydl_opts)

        for link in links:
            yt_opts_instance.download([link])

    elif choice == "3":
        youtube = GetList.authenticate_youtube()
        video_urls = GetList.get_watch_later_videos(youtube)
        # playlists = GetList.get_all_playlists(youtube)

        # for video in video_urls:
        #     if isinstance(video, dict):
        #         if isinstance(video, dict) and "snippet" in video and "title" in video["snippet"]:
        #             print(video["snippet"]["title"])

        print("上記の動画リストを対象に処理を実行します。\n")
        continue

    elif choice == "4":
        exit()

    else:
        print("1,2,3,4のどれかを選択してください。")
        exit()
