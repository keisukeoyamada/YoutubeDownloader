# YoutubeDownloader

## pipの一括インストールオプション: -r requirements.txt
以下のコマンドで設定ファイルrequirements.txtに従ってパッケージが一括でインストールされる。
```s
pip install -r requirements.txt
```
## 事前準備
事前準備を参照

## GetListfromYT_Auth.py
Youtubeアカウントから動画リストを取得してくる
取得した動画URLのリストをdownload_list.jsonとして出力する

## YT_dL.py
download_list.jsonに記載の動画リストに基づいて、動画（mp4）をダウンロードする

## 事前準備
Google CloudでOAuthクライアントIDを取得

Google Cloud Consoleにアクセスし、プロジェクトを選択または作成します。
「認証情報」セクションで「認証情報を作成」→「OAuthクライアントID」を選択。
アプリケーションの種類を「デスクトップアプリケーション」として設定し、クライアントIDとクライアントシークレットを取得します。

### FYI
https://qiita.com/pasaremon/items/df461947344bb76ee25f

