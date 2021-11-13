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
twitterapi                2.7.7                    pypi_0    pypi
urllib3                   1.26.7                   pypi_0    pypi
vc                        14.2                 h21ff451_1
vs2015_runtime            14.27.29016          h5e58377_2
wheel                     0.37.0             pyhd3eb1b0_1
wincertstore              0.2              py38haa95532_2
```

## 使い方
後述の `Client ID` と `Client Secret` を `.env.example` のノリで `.env` ファイルに記述し、上述の環境を用意して `caitsith.py` を実行する。

結果：現ユーザのLiked Songsの内容が列挙される。


## 作り方メモ
### Spotify

[Spotify][spotify]にログインし、[Spotify for Developers Dashboard][spotify-dev-dashboard]にSpotifyアカウントでログインしたら、 `CREATE AN APP` からアプリを作成。

- `Client ID` と `Client Secret` （"SHOW CLIENT SECRET" をクリックで表示）が後で必要になる。
- "EDIT SETTINGS" で設定する `Redirect URIs` も一つ追加しておく。ここでは `http://localhost:8888/callback` を使用している（正当性は不明）。

### Slack

Slackへの投稿を利用しないならこの項は不要。

### Twitter

Twitterへの投稿を利用しないならこの項は不要。

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
- `pip install TwitterAPI`：Twitter APIの利用

### Visual Studio Code
Pythonのコードを実行するにはまず `.py` ファイルを作成し、左下の `Python x.x.xx 64-bit ('hogehoge': conda)` という箇所をクリックして仮想環境を選択する。あとはF5を押すとDebug Configurationが出てくるが、そのままEnterを押せば `Python File` として実行される。

また、APIのトークンなど公開したくない文字列は、リポジトリルートフォルダ直下に `.env` ファイルを置き、その中に環境変数として記述するとよい。
- `.gitignore` に `.env` を記述しておけばコミットなどに含まれなくなる。今回は `.gitignore` 作成時に既定で記述されていた。
- どのような環境変数を用いているかを公開したい場合は、 `.env.example` などといったファイルに `.env` の内容を（**実際の値は伏せて**）記述すればよい。
- 実際にPythonコード内で `.env` の内容を環境変数として扱いたい場合は、 `python-dotenv` の関数 `load_dotenv()` を呼び出す。

#### 環境変数：Spotipy

Spotify for Developers Dashboardのアプリの `Client ID`, `Client Secret`, `Redirect URI` を `SPOTIPY_CLIENT_ID`, `SPOTIPY_CLIENT_SECRET`, `SPOTIPY_REDIRECT_URI` として通しておく。これにより認証の際にこれらを引数に渡す手間が省ける。
- `SPOTIFY_XXX_XXX` でないことに注意。すぽてぃぱい。

#### 環境変数：Slack

aaaa

### その他

Spotify Web APIの動作・必要scopeの確認には[Spotify for Developers Console][spotify-dev-console]が便利。返り値も確認できる。

## Spotipyメモ

公式ドキュメントの翻訳とかやが…

すべてのメソッドはユーザ認証必須なので、Dashboardから認証情報を得ておく必要がある。

認証の流れは2つある。

- **Authorization Code flow** は、ユーザーが一度ログインするだけの長時間稼働のアプリケーションに適しています。アクセストークンを提供し、それをリフレッシュすることができます。
  - Dashboardでredirect URIを追加しておく必要がある。
- **Client Credentials flow** により、Spotify Web APIへのリクエストを認証し、Authorization Codeフローよりも高いレート制限を得ることが可能になります。


### Authorization Code Flow

このフローは、ユーザーが一度だけ許可を与えるような長時間稼働のアプリケーションに適しています。このフローでは、リフレッシュ可能なアクセストークンを提供します。トークンの交換には秘密鍵の送信を伴うため、ブラウザやモバイルアプリなどのクライアントからではなく、バックエンドサービスなどの安全な場所で実行してください。

`SpotifyOAuth`クラスを使う。Redirect URIは `http://localhost:8888/callback` とかを指定しておけばよい？

で現在のユーザの保存した曲のリストを取得したり色々する際にOAuth Tokenの適切なscopeをリクエストする必要がある（scopeが足りないと想定する動作が許されなかったりする）が、その確認には[Spotify for DevelopersのConsoleページ](https://developer.spotify.com/console/)がおすすめ。何をすれば何が返ってくるのかの確認もできる。

### Client Credentials Flow

Client Credentialsフローは、サーバー間認証で使用されます。ユーザー情報にアクセスしないエンドポイントのみがアクセスできます。アクセストークンを使用しないWeb APIへのリクエストと比較して、より高いレート制限が適用されるという利点があります。

`SpotifyClientCredentials` クラスを使う。ユーザ情報へのアクセスはできない。Redirect URIは不要。


## その他メモ

[Pythonスクリプトをexe化する](https://www.python.ambitious-engineer.com/archives/3306)という記事がある。

[これ](https://community.spotify.com/t5/Your-Library/How-to-share-the-quot-Liked-Songs-quot-Playlist/td-p/4828788)によると、Liked Songsをシェアする方法はない。アクセスする方法はなさそう？  
あるいはsaved_tracks関連でいける？


<!-- Markdown links -->

[github-desktop]: https://desktop.github.com/ "GitHub Desktop"
[github-desktop-documents]: https://docs.github.com/ja/desktop "GitHub Desktopのドキュメント"
[github-desktop-documents-readme-md]: https://docs.github.com/ja/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes "GitHub Desktopのドキュメント：README.md"
[github-writing-markdown]: https://gist.github.com/LambdaNote/0d33b7d8284a3c99cffd1a5aa83c115f "GitHub: 記事の書き方"
[gitignore-qiita-1]: https://qiita.com/inabe49/items/16ee3d9d1ce68daa9fff "Qiita: .gitignore の書き方"
[gitignore-qiita-2]: https://qiita.com/anqooqie/items/110957797b3d5280c44f "Qiita: [Git] .gitignoreの仕様解説"
[python-environment-variable]: https://www.twilio.com/blog/environment-variables-python-jp "twilio BLOG: Pythonで環境変数を活用する"
[python-dotenv-documents]: https://pypi.org/project/python-dotenv/ "python-dotenv 公式ドキュメント"
[spotify]: https://www.spotify.com/ "Spotify"
[spotify-dev-console]: https://developer.spotify.com/console/ "Spotify for Developer Console"
[spotify-dev-dashboard]: https://developer.spotify.com/dashboard/ "Spotify for Developer Dashboard"
[spotify-webapi-tutorial]: https://developer.spotify.com/documentation/web-api/quick-start/ "Spotify Web API Tutorial"
[spotipy-documents]: https://spotipy.readthedocs.io/en/2.19.0/ "Spotipy 公式ドキュメント"
