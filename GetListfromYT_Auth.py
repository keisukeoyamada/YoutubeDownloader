import json
import os
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError


# JSONファイルパス
JSON_FILE = "download_list.json"
CREDENTIALS_FILE = "client_secret.json"  # Google Cloudでダウンロードしたクライアントシークレット

# YouTube APIスコープ
SCOPES = ["https://www.googleapis.com/auth/youtube"]
# SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

def authenticate_youtube():
    creds = None
    # トークンファイルを確認し、再利用可能な認証情報があるかチェック
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # 認証情報がない場合、または期限切れの場合に再認証
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # トークンを保存
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)

def get_watch_later_videos(youtube):
    # 固定ID "WL" を使用して「後で見る」リストを取得
    watch_later_id = "PLmYRaZB-FBUXpSj0hiAYSgI_44hjjoXgN"
    # watch_later_id = "WL"

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
        print("API Response:", json.dumps(response, indent=2, ensure_ascii=False))  # デバッグ用出力
        for item in response.get("items", []):
            video_id = item["snippet"]["resourceId"]["videoId"]
            video_urls.append(f"https://www.youtube.com/watch?v={video_id}")

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return video_urls

def backup_existing_file(file_path):
    if os.path.exists(file_path):
        backup_name = f"{os.path.splitext(file_path)[0]}_backup_at_{datetime.now().strftime('%Y-%m-%d')}.json"
        os.rename(file_path, backup_name)
        print(f"既存のファイルをバックアップしました: {backup_name}")

def append_with_diff(file_path, urls):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"urls": []}
    
    # 差分を計算
    existing_urls = data["urls"]
    # existing_urls = set(data["urls"])
    new_urls = [url for url in urls if url not in existing_urls]
    
    if new_urls:
    
        # 差分を追加
        data["urls"].extend(new_urls)
        
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        
        print(f"{len(new_urls)}件の新しいURLを追加しました。")
        return True  # 差分ありを示す
    else:
        print("更新差分がありません。")
        return False  # 差分なしを示す

def get_all_playlists(youtube):
    playlists = []
    next_page_token = None
    while True:
        response = youtube.playlists().list(
            part="snippet",
            mine=True,
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        playlists.extend(response.get("items", []))
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
    return playlists

# def main():
#     print("全プレイリストを取得しています...")
#     try:
#         youtube = authenticate_youtube()
#         playlists = get_all_playlists(youtube)
#         if playlists:
#             print("取得したプレイリスト:")
#             for playlist in playlists:
#                 print(f"- {playlist['snippet']['title']} (ID: {playlist['id']})")
#         else:
#             print("プレイリストが見つかりませんでした。")
#     except HttpError as e:
#         print("Google APIでエラーが発生しました。")
#         print(e)

def main():
    print("後で見るリストのURLを取得しています...")
    try:
        youtube = authenticate_youtube()
        playlists = get_all_playlists(youtube)
        if playlists:
            print("取得したプレイリスト:")
            for playlist in playlists:
                print(f"- {playlist['snippet']['title']} (ID: {playlist['id']})")
        else:
            print("プレイリストが見つかりませんでした。")    

        # youtube = authenticate_youtube()
        video_urls = get_watch_later_videos(youtube)
        if video_urls:
            # バックアップを作成
            backup_existing_file(JSON_FILE)
            # 差分を比較して追加
            updated = append_with_diff(JSON_FILE, video_urls)
            if not updated:
                print("新しいURLは追加されませんでした。")
        else:
            print("URLの取得に失敗しました。")
    except HttpError as e:
        print("Google APIでエラーが発生しました。")
        print(e)
        if "The app is currently in testing mode" in str(e):
            print("エラー: このアプリはテストモードです。テスターに登録されていない場合は、Google Cloud Consoleで自分のアカウントをテストユーザーに追加してください。")

if __name__ == "__main__":
    main()
