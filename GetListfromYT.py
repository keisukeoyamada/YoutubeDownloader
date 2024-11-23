import json
from googleapiclient.discovery import build

# YouTube Data APIキーを設定
API_KEY = "AIzaSyA09IEHJDVU0BMSL5mWE_iwAcGfcwTQ_dg"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# JSONファイルパス
JSON_FILE = "watch_later_urls.json"

def get_watch_later_videos(api_key):
    # YouTube APIのクライアントを作成
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=api_key)

    # "後で見る"プレイリストのIDを取得
    response = youtube.playlists().list(part="snippet", mine=True).execute()
    watch_later_id = None
    for playlist in response.get("items", []):
        if playlist["snippet"]["title"] == "後で見る":
            watch_later_id = playlist["id"]
            break

    if not watch_later_id:
        print("後で見るリストが見つかりませんでした。")
        return []

    # "後で見る"リストの動画を取得
    video_urls = []
    next_page_token = None
    while True:
        response = youtube.playlistItems().list(
            part="snippet",
            playlistId=watch_later_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in response.get("items", []):
            video_id = item["snippet"]["resourceId"]["videoId"]
            video_urls.append(f"https://www.youtube.com/watch?v={video_id}")

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return video_urls

def append_to_json(file_path, urls):
    try:
        # 既存のJSONデータを読み込み
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        # ファイルが存在しない場合は新規作成
        data = {"urls": []}

    # 重複を避けてURLを追加
    for url in urls:
        if url not in data["urls"]:
            data["urls"].append(url)

    # JSONファイルに書き込み
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def main():
    print("後で見るリストのURLを取得しています...")
    video_urls = get_watch_later_videos(API_KEY)
    if video_urls:
        append_to_json(JSON_FILE, video_urls)
        print(f"{len(video_urls)}件のURLを {JSON_FILE} に追加しました。")
    else:
        print("URLの取得に失敗しました。")

if __name__ == "__main__":
    main()
