# SpotifyApp
 Spotify Web APIとやらを使い、SpotifyをPythonでなんかする。

## やりたいこと

自分のLiked Songsから毎日ランダムに1曲選び、それを解説するためのアプリを作る。

## 用語諸々
### Spotify

https://www.spotify.com/

> Spotifyは数千万の楽曲とポッドキャストを楽しめるオーディオストリーミングプラットフォームです。

みんなが曲を聴くやつ。

### Spotify for Developers

https://developer.spotify.com/

なんかAPIが存在していてなんかできるらしい。

## 実行環境
- Windows 10 Home
- Anaconda 4.10.1
- `conda list` ：

```
# Name                    Version                   Build  Channel
ca-certificates           2021.10.26           haa95532_2
certifi                   2021.10.8        py38haa95532_0
charset-normalizer        2.0.7                    pypi_0    pypi
idna                      3.3                      pypi_0    pypi
oauthlib                  3.1.1                    pypi_0    pypi
openssl                   1.1.1l               h2bbff1b_0
pip                       21.0.1           py38haa95532_0
python                    3.8.12               h6244533_0
python-dotenv             0.19.2                   pypi_0    pypi
requests                  2.26.0                   pypi_0    pypi
requests-oauthlib         1.3.0                    pypi_0    pypi
setuptools                58.0.4           py38haa95532_0
six                       1.16.0                   pypi_0    pypi
slack-bolt                1.10.0                   pypi_0    pypi
slack-sdk                 3.11.2                   pypi_0    pypi
spotipy                   2.19.0                   pypi_0    pypi
sqlite                    3.36.0               h2bbff1b_0
tweepy                    4.3.0                    pypi_0    pypi
twitterapi                2.7.7                    pypi_0    pypi
urllib3                   1.26.7                   pypi_0    pypi
vc                        14.2                 h21ff451_1
vs2015_runtime            14.27.29016          h5e58377_2
wheel                     0.37.0             pyhd3eb1b0_1
wincertstore              0.2              py38haa95532_2
```

## 使い方
環境変数を `.env.example` のノリで `.env` ファイルに記述し、上述の環境を用意して `caitsith.py` を実行する。

そして下のやつを見ていい感じにやる。

ドライブ上にも何かjsonファイルが必要そう。

結果：現SpotifyユーザのLiked Songsの中から一つをランダムに選び、SlackとTwitterで自分に対して曲の紹介を要求するメンションが飛んでくる。


## 自分用メモ
### 公式系

- [Spotify for Developers Dashboard][spotify-dev-dashboard]
- [Slack Your Apps][slack-apps]
- [Twitter Developer Apps][twitter-apps]
- [Heroku][heroku]

### ドキュメント系

- [Spotipy Documentation][spotipy-documents]
- [slack-boltのガイド？][slack-bolt-python-guides]
- [Boltでアプリを作る][slack-build-app-with-bolt]
- [Slackでリッチなテキストを書く][slack-rich-message]
- [Tweepy Documentation][tweepy-documents]
- [Tweepy日本語ドキュメント（古い）][tweepy-documents-ja-old]


## 作り方メモ
### Spotify

[Spotify][spotify]にログインし、[Spotify for Developers Dashboard][spotify-dev-dashboard]にSpotifyアカウントでログインしたら、 `CREATE AN APP` からアプリを作成。

- `Client ID` と `Client Secret` （"SHOW CLIENT SECRET" をクリックで表示）が後で必要になる。
- "EDIT SETTINGS" で設定する `Redirect URIs` も一つ追加しておく。ここでは `http://localhost:8888/callback` を使用している（正当性は不明）。

### Slack

Slackへの投稿を利用しないならこの項は不要。また手順は将来変更される可能性も。

Slack APIの[Your Apps][slack-apps]から `Create New App` でアプリを作成する。 `app Manifest` が何かわからないならとりあえず `From scratch` を選択して後から権限などの設定を行えばよい。アプリの名前と使用するWorkspaceを入力して `Create App` 。

- Settings > App Manifestからアプリの説明や権限などの追加が行える。上部の `View Documentation` で調べながら頑張る。
- Settings > Incoming WebhooksからIncoming Webhooksの設定を行いそう。
- Settings > OAuth & Permissionsから `Bot User OAuth Token` などの確認が行える。
- 必要な権限とかは頑張って調べて頑張る。

### Twitter

Twitterへの投稿を利用しないならこの項は不要。また手順は将来変更される可能性も。

投稿に利用したいTwitterアカウントの携帯電話番号の登録を済ませておき、[Twitter Developer Appsみたいなやつ][twitter-apps]にアクセスして `Create an app` をクリック。大体でよいのでAPIの使用目的などを入力（英語あり）し、審査が終わるとTokenなどが表示されるので控えを取る。Developer PortalのProject画面にあるAppの鍵マークから `Access Token` などを生成してこれも控えを取る。

- 普段使っているものとは別のアカウントでツイートしたい場合は新しくTwitterアカウントを作成する。電話番号は普段使っているものと同じ番号を使用してよい。
- Token系は一度しか表示されず、忘れた場合はRegenerateを行う必要がある。
- ProjectやApp Detailsの編集は少し時間が経つと行えるようになる？（鉛筆マーク）
- Tweetを行いたい場合はアプリのSettingから `App permissions` を `Read` から `Read and write` にする必要がありそう。
  - 各種トークンのRegenerateも忘れないこと。

また、Twitterの自動システムのスパム誤認によるAPI凍結を食らうこともある。その場合はサポートから何か送りましょう。

### Google Drive API

設定ファイルをGoogle Driveに保存し、Herokuアプリからアクセスするために使用している。ローカルで運用するなら不要。

色々調べたが、結局[Googleの公式QuickStart](https://developers.google.com/drive/api/v3/quickstart/python)をベースにやることになった。

- PyDrive2だと設定ファイルをGitHub上で公開せずに済む方法が見つからなかった。
- PyDrive2の依存関係に含まれていない `google-auth-oauthlib` の中の関数を使う方法でやることにする。

まずPrerequisitesその1として、[プロジェクトを作成してAPIを有効化](https://developers.google.com/workspace/guides/create-project)する。

- [Google Developers Console](https://console.developers.google.com/)にアクセスし、左メニューの「APIとサービス」>「ダッシュボード」を選択してプロジェクトを作成する。
- ダッシュボード上側の「APIとサービスの有効化」をクリックし、Google Drive APIを検索するなりして見つけて有効化する。

次にPrerequisitesその2として、[認証情報の作成](https://developers.google.com/workspace/guides/create-credentials)を行う。

- ここでは認証情報の作成に「OAuthクライアントID」を使用するので、OAuth 同意画面の作成が必要になり、そちらを先に行う。設定は「APIとサービス」>「OAuth 同意画面」から。
  - まずUser Typeの選択の画面になるが、Google Workspaceユーザでないと `内部` は選択できず、 `外部` を選択することになる。 `作成` を押す。
  - アプリ登録の編集のOAuth同意画面の設定が表示されるので、必須のアプリ名やメールアドレス、メールアドレスを入力。
  - 次にスコープの画面になるが、これは無視して良さそう。設定するなら[これ](https://developers.google.com/workspace/guides/identify-scopes)を参考に。
  - テストユーザーは、恐らくサービスアカウントを使用しないのであればここに登録したユーザーのみが使えるとかだと思う。今はまだ使っていない。
- 「APIとサービス」>「認証情報」から「認証情報を作成」を選択。ここでは「OAuthクライアントID」を使用。
  - アプリケーションの種類は、公式QuickStartに準じて「デスクトップアプリ」を選択。
  - 「クライアント ID」と「クライアント シークレット」が表示されるので控えをとっておく。
  - あるいはjsonファイルをダウンロードし、QuickStartに従って `client_secret_XXXXXX....json` から `credentials.json` にリネームする。 `client_secret.json` でもよいがその場合コード中の文字列もこちらに変更しておくこと。

[QuickStart](https://developers.google.com/drive/api/v3/quickstart/python)を行う。必要なライブラリをインストールし、 `quickstart.py` を作成してコードをコピーして実行する。

- `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`
- 自分の環境では既に `pip install PyDrive2` を行っており、新たにインストールされたのは `google-auth-oauthlib` のみだった。
- コード実行の際、初期状態（ `token.json` が存在しない状態）ではブラウザが開いて同意画面が表示される。

このコードを `google_drive.py` かなんかにコピーして改造していくが、まず必要なトークンの入手を行う。

- まず `SCOPES` を変更して `token.json` を削除してからコードを実行し、同意画面の表示と新しい `token.json` の入手を済ませておく。
- スコープについて、[Drive API (V3)のドキュメント](https://developers.google.com/drive/api/v3/about-auth)によると `https://www.googleapis.com/auth/drive.appdata` で `Application Data folder` というアプリ固有のフォルダ内のファイルにフルアクセスできるらしい。通常は設定ファイルなどをここに置く。
  - しかしどうやらユーザーからは見られない模様（[参考](https://stackoverflow.com/questions/22832104/how-can-i-see-hidden-app-data-in-google-drive)）。一応確認などのためにLiked Songsとかのファイルはユーザーから見られるようにしておきたいので断念。
- 結局全ドライブファイルにアクセスできる `https://www.googleapis.com/auth/drive` を使用することにした。

そして `credentials.json` (`client_secret.json`) や `token.json` といったトークン情報が入ったファイルをGitHub上に公開しないように、コードを改変していく。

- リネームした `credentials.json` と `token.json` の中身を **そのまま環境変数にブチ込む** 。[参考](https://qiita.com/yume_yu/items/171b04fb81dd67604683)
  - キーは適当に `GOOGLE_CLIENT_SECRET_JSON` と `GOOGLE_TOKEN_JSON` とかで。
- Pythonコードで `import os, json` と `from dotenv import load_dotenv` して `load_dotenv()` する。
  - でも `load_dotenv()` ってHeroku上のプログラムにはいらなくね？まあええか
- また、 `Credentials.from_authorized_user_file` を `Credentials.from_authorized_user_info` に、 `InstalledAppFlow.from_client_secrets_file` を `InstalledAppFlow.from_client_config` に変更し、jsonファイルの代わりに `os.environ['環境変数のキー']` を `json.loads()` に突っ込んだものを第一引数としておく。第二引数は元の関数と同じく `SCOPES` でよい。
- `token.json` ファイルの存在確認を、 `os.environ` 辞書における `GOOGLE_TOKEN_JSON` キーの存在確認に変更。
- また、 `token.json` ファイルを保存するところを `os.environ['GOOGLE_TOKEN_JSON']` に `creds.to_json()` を代入するものに直しておく。
  - 但しこれが意味のあるコードなのかは不明（プログラム中の環境変数への変更はそのプログラム中においてのみ有効らしい：[参考](https://note.nkmk.me/python-os-environ-getenv/))）。

ここからはAPIの動作を実装する。この時サービス動作のコードを別メソッドに分離しておくとやりやすいかもしれない。

- 必要なメソッドとかはGoogle Drive for Developersの[Drive API (V3)](https://developers.google.com/drive/api/v3/about-files)の該当箇所とかを見てくれ
  - あるいは[ここ](https://zenn.dev/wtkn25/articles/python-googledriveapi-operation)とかちょっと分かりやすいか？
- なおダウンロード/アップロードには `from googleapiclient.http import MediaIoBaseDownload` `from googleapiclient.http import MediaFileUpload` が必要なので注意。公式ドキュメントには書かれていない。
- なおドライブからのダウンロードについては[これ](https://udon.little-pear.net/python-google-drive-api/#reference1)を見よう。公式だとできなかった。


[参考](https://news.mynavi.jp/article/zeropython-16/)


### GitHub Desktop

ダウンロードは[こちら][github-desktop]、ドキュメントは[こちら][github-desktop-documents]。

File > New Repositoryなどで（ローカル？）リポジトリを作成。指定したフォルダ直下にリポジトリ名のフォルダが作成される。
- `README.md` はお好みで。書き方の[参考][github-desktop-documents-readme-md]・Markdown書き方[参考][github-writing-markdown]。
- `.gitignore` はPythonを使うのでPythonを指定。[参考1][gitignore-qiita-1]、[参考2][gitignore-qiita-2]。
- ライセンスはよく分からないので今は設定せず。

Repository > Open in Visual Studio CodeなどでVS Codeでの作業が行える。ファイル変更をローカルリポジトリに反映させる場合はcommitを行い、ローカルリポジトリの変更をリモートリポジトリに反映させる場合はPush originを行う。
- Pushは初回はPublish repositoryになっており、これによりGitHubサイトへの公開が行える。
- `Keep this code private` にチェックを入れたままPublishした場合、Publicに変更するにはサイトの方から設定のDanger Zoneで公開設定を変更する必要がある。
  - Danger Zone、ちょっと怖い。
- ちなみにVS CodeでのMarkdownのプレビューは「Ctrl+K, V」。

### Anaconda
Python3.8とかの新しい仮想環境を作成し、適宜パッケージをインストールする。
- `pip install spotipy --upgrade`：Spotify Web APIの利用
- `pip install python-dotenv`：環境変数の使用。[参考][python-environment-variable]、[公式ドキュメント][python-dotenv-documents]。
- `pip install slack-bolt`：2021年現在新しめのslackbot等パッケージ。 `slack-sdk` も同時にインストールされる
- `pip install TwitterAPI`：Twitter APIの利用（いらないかも）
- `pip install tweepy`：Twitter APIのラッパー？

### Visual Studio Code
Pythonのコードを実行するにはまず `.py` ファイルを作成し、左下の `Python x.x.xx 64-bit ('hogehoge': conda)` という箇所をクリックして仮想環境を選択する。あとはF5を押すとDebug Configurationが出てくるが、そのままEnterを押せば `Python File` として実行される。

また、APIのトークンなど公開したくない文字列は、リポジトリルートフォルダ直下に `.env` ファイルを置き、その中に環境変数として記述するとよい。
- `.gitignore` に `.env` を記述しておけばコミットなどに含まれなくなる。今回は `.gitignore` 作成時に既定で記述されていた。
- どのような環境変数を用いているかを公開したい場合は、 `.env.example` などといったファイルに `.env` の内容を（**実際の値は伏せて**）記述すればよい。
- 実際にPythonコード内で `.env` の内容を環境変数として扱いたい場合は、 `python-dotenv` の関数 `load_dotenv()` を呼び出す。

#### 環境変数：アプリ

アプリで使用するコンフィグファイル、SpotifyのLiked Songsを格納するファイル、これまで選択した曲を格納するファイルの名前を環境変数にブチ込む。

#### 環境変数：Spotipy

[Spotify for Developers Dashboard][spotify-dev-dashboard]のアプリの `Client ID`, `Client Secret`, `Redirect URI` を `SPOTIPY_CLIENT_ID`, `SPOTIPY_CLIENT_SECRET`, `SPOTIPY_REDIRECT_URI` として通しておく。これにより認証の際にこれらを引数に渡す手間が省ける。
- `SPOTIFY_XXX_XXX` でないことに注意。すぽてぃぱい。
- `SPOTIPY_REDIRECT_URI` はとりあえず `http://localhost:8888/callback` を指定している。

#### 環境変数：Slack

[Slackアプリ][slack-apps]から選択したアプリの `OAuth & Permissions` に `Bot User OAuth Token` があったのでそれを `SLACK_BOT_TOKEN` とか適当に通す。

#### 環境変数：Twitter

アプリ作成などに控えを取っていた各種トークン、 `API Key`, `API Key Secret`, `Bearer Token`, `Access Token`, `Access Token Secret` を各々適当に `TWITTER_` とかを頭につけて[アッパースネークケース][naming-convention-cases-upper-snake]とかで通す。

- `API Key`, `API Key Secret` はかつて `Consumer Key`, `Consumer Secret` と呼ばれていた模様。古い記事だとそちらの表記になっている。
- トークンを忘れたり `Access` 系のgenerateを忘れていたりした場合は、[Developer Portal][twitter-apps]（既にアプリを作成した場合）の該当プロジェクトの下の方にある "Apps" の該当アプリの右側にある鍵マークからRegenerateやGenerateが行える（確認はできない）。

#### 環境変数：Google Drive API
`credentials.json` あるいは `client_secret.json` と `token.json` の内容をそれぞれ `GOOGLE_CLIENT_SECRET_JSON`, `GOOGLE_TOKEN_JSON` にブチ込む。詳細は上のやつを見てください。

### Heroku

アカウントを作成し、アプリを作成し、何かPythonを設定して色々やる。詳しくは[こっちのリポジトリ](https://github.com/motakine/SlackBolt)に書いてあるからそれ読んで。

加えてこのアプリでは定期実行を行いたいのでその設定を行う。[参考](https://qiita.com/pythonista/items/2eab3e3acad88c5b759e)
- アプリのダッシュボードの `Resources` から `Find more add-ons` を選択するか直下の検索フォームから `Heroku Scheduler` を選ぶ。
- `Plan name` が `Standard - Free` であることを確認し、 `Provision` を押下。 `Submit Order Form` かもしれない。
- 追加された `Heroku Schedular` から管理画面を開き、初なら `Create job` 、経験済みなら `Add Job` からスケジューリングを行う。
  - 10分毎、1時間毎（開始時刻は10分刻み）、1日毎（開始時刻は30分刻み）から間隔を設定、実行コマンドも設定。
- `Save job` でスケジュールが作成される。


### その他

Spotify Web APIの動作・必要scopeの確認には[Spotify for Developers Console][spotify-dev-console]が便利。返り値も確認できる。

configとかのjsonファイルのローカルでの保存場所をjsonフォルダ以下にしようと思ったけどGoogle Driveでも同じパスを指定してたせいでエラーが出て面倒になったので断念。


## その他メモ

[一番分かりやすい OAuth の説明](https://qiita.com/TakahikoKawasaki/items/e37caf50776e00e733be)とかいうQiitaの記事がある。SlackやTwitterのbotを作るときの参考の参考くらいに。

[Pythonスクリプトをexe化する](https://www.python.ambitious-engineer.com/archives/3306)という記事がある。

[これ](https://community.spotify.com/t5/Your-Library/How-to-share-the-quot-Liked-Songs-quot-Playlist/td-p/4828788)によると、Liked SongsをSpotifyでシェアする方法はない。

[Python命名規則一覧](https://qiita.com/naomi7325/items/4eb1d2a40277361e898b)

Pythonの日付操作は[ここ](https://qiita.com/papi_tokei/items/43b1d15a6694f576486c)[らへ](https://note.nkmk.me/python-datetime-now-today/)[ん](https://note.nkmk.me/python-datetime-usage/)とかを参照。比較は[ここ](https://qiita.com/Alice1017/items/4ce5be3f46aa34f9f900)。

<!-- Markdown links -->

[github-desktop]: https://desktop.github.com/ "GitHub Desktop"
[github-desktop-documents]: https://docs.github.com/ja/desktop "GitHub Desktopのドキュメント"
[github-desktop-documents-readme-md]: https://docs.github.com/ja/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes "GitHub Desktopのドキュメント：README.md"
[github-writing-markdown]: https://gist.github.com/LambdaNote/0d33b7d8284a3c99cffd1a5aa83c115f "GitHub: 記事の書き方"
[gitignore-qiita-1]: https://qiita.com/inabe49/items/16ee3d9d1ce68daa9fff "Qiita: .gitignore の書き方"
[gitignore-qiita-2]: https://qiita.com/anqooqie/items/110957797b3d5280c44f "Qiita: [Git] .gitignoreの仕様解説"
[heroku]: https://www.heroku.com/ "Heroku"
[python-environment-variable]: https://www.twilio.com/blog/environment-variables-python-jp "twilio BLOG: Pythonで環境変数を活用する"
[python-dotenv-documents]: https://pypi.org/project/python-dotenv/ "python-dotenv 公式ドキュメント"
[slack-apps]: https://api.slack.com/apps "Slack: Your Apps"
[slack-bolt-python-guides]: https://slack.dev/bolt-python/ja-jp/tutorial/getting-started "Slack: Bolt for Pythonガイド"
[slack-build-app-with-bolt]: https://api.slack.com/start/building/bolt-python "Building an app with Bolt for Python"
[slack-rich-message]: https://api.slack.com/messaging/composing/layouts "Creating rich message layouts"
[spotify]: https://www.spotify.com/ "Spotify"
[spotify-dev-console]: https://developer.spotify.com/console/ "Spotify for Developer Console"
[spotify-dev-dashboard]: https://developer.spotify.com/dashboard/ "Spotify for Developer Dashboard"
[spotify-webapi-tutorial]: https://developer.spotify.com/documentation/web-api/quick-start/ "Spotify Web API Tutorial"
[spotipy-documents]: https://spotipy.readthedocs.io/en/2.19.0/ "Spotipy 公式ドキュメント"
[tweepy-documents]: https://docs.tweepy.org/en/latest/index.html "Tweepy Documentation"
[tweepy-documents-ja-old]: https://kurozumi.github.io/tweepy/index.html "Tweepyドキュメント(v3.6.0)"
[twitter-apps]: https://developer.twitter.com/en/apps/ "Twitter Developer Apps"

[naming-convention-cases-upper-snake]: https://qiita.com/terra_yucco/items/ec437c6005932fd73fb9#%E3%82%A2%E3%83%83%E3%83%91%E3%83%BC%E3%82%B9%E3%83%8D%E3%83%BC%E3%82%AF%E3%82%B1%E3%83%BC%E3%82%B9--upper-snake-case
