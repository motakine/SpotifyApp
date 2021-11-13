# SpotifyApp
 Spotify Web APIとやらを使い、SpotifyをPythonでなんかする。

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
openssl                   1.1.1l               h2bbff1b_0
pip                       21.0.1           py38haa95532_0
python                    3.8.12               h6244533_0
python-dotenv             0.19.2                   pypi_0    pypi
requests                  2.26.0                   pypi_0    pypi
setuptools                58.0.4           py38haa95532_0
six                       1.16.0                   pypi_0    pypi
spotipy                   2.19.0                   pypi_0    pypi
sqlite                    3.36.0               h2bbff1b_0
urllib3                   1.26.7                   pypi_0    pypi
vc                        14.2                 h21ff451_1
vs2015_runtime            14.27.29016          h5e58377_2
wheel                     0.37.0             pyhd3eb1b0_1
wincertstore              0.2              py38haa95532_2
```

## 使い方
後述の `Client ID` と `Client Secret` を `.env.example` のノリで `.env` ファイルに記述し、上述の環境を用意して `caitsith.py` を実行する。

結果：現ユーザのLiked Songsの内容が列挙される。


## 作る手順メモ
### Spotify

- Spotifyにログイン

まずSpotifyにログインし、Spotify for Developersの [Dashboard][spotify-dashboard] にもSpotifyアカウントを使ってログインする。次に `CREATE AN APP` からアプリを作成する。  
なお `Client ID` と "SHOW CLIENT SECRET" クリックで表示される `Client Secret` は後で必要になる。晒すとヤバそう。

折角なのでGitHubを使う。GitHub Desktopを起動して（ローカル？）リポジトリを作成。選択したローカルフォルダ直下に指定したリポジトリ名（今回はSpotifyApp）のフォルダができるらしい。README.mdはつけて `.gitignore` もPythonを選択。ライセンスはまあ後でええやろ。

AnacondaでPython3.8の新しい仮想環境を作り、Anaconda Promptで `pip install spotipy --upgrade` [^1]。また環境変数を使うために `pip install python-dotenv` もしとく[^2]。

でなんかGitHub Desktop側でリポジトリフォルダをVS Codeで開くみたいなのがあったのでそれで作業を行う。都度 `README.md` にやったことをメモしていく。ちなみにVS CodeでMarkdownのプレビューは「Ctrl+K, V」で行える。

また、後々 `Client ID` とか `Client Secret` とかをコード内で使うことになるが、そのままコードに組み込んでGitHubとかで公開するとマズいので、`.env`ファイル内に環境変数として記述しておき、コード内では`python-dotenv`の関数を使うことにする。  
但し`.env`ファイルをGitHubに公開してしまうとそれもマズいので、`.gitignore`に`.env`の行が含まれていることを確認する（リポジトリを作成するときの設定でデフォで入ってるはず）。必要な環境変数は[Spotify Web APIのクイックスタート](https://developer.spotify.com/documentation/web-api/quick-start/)を参照した。  
どんな環境変数を使っているかをGitHubに公開したい場合は`.env.example`ファイルを作成してそこに適当に書く（本物のキーを入力しないように）[^2]。  
なおSpotipyを使う場合は `SPOTIPY_CLIENT_ID`, `SPOTIPY_CLIENT_SECRET`, `SPOTIPY_REDIRECT_URI` の3つを環境変数に追加しておいたほうが良さそうな雰囲気（SPOTIFYではなくSPOTI **P** Y)）。

`caitsith.py` とか名前は何でもいいので `.py` ファイルを作成する。なお左下の `Python x.x.xx 64-bit ('hogehoge': conda)` の箇所をクリックすれば仮想環境を選択できる。で `print ("Hello, Python!")` でもしてF5を押すとDebug Configurationとやらが出てくるが、そのままEnterを押せば `Python File` として実行してくれそう。[^1]

あとは頑張って色々見て[^1][^2][^8]、`.py`ファイルをいじって実行してください。

## GitHubいろいろ
今回使用しているのはいつ入れたか忘れたGitHub Desktop[^3]。コマンドラインは嫌や！

File > New Repositoryしてからローカルフォルダ指定・README.md[^4][^5]・`.gitignore`[^6][^7]・ライセンスをなんやかんやしてリポジトリ作成。今後変更があった場合は適宜（ローカルリポジトリに）commitを行う。

なおこのままだと外部には公開されていないので、Publish repositoryでGitHubのサイトに公開する。このとき`Keep this code private`にチェックを入れたままだと他人が見られないので注意。後からサイトにアクセスしてSettingのDanger Zoneから公開設定を変更できるが赤くて怖いので注意。

以降ローカルの変更をcommitしたあとにリモートにも反映させる場合は、Publish repositoryがPush Originになっているのでそれで。


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


[^1]: [Spotipy公式ドキュメント](https://spotipy.readthedocs.io/en/2.19.0/)  
[^2]: [twilio BLOG: Pythonで環境変数を活用する](https://www.twilio.com/blog/environment-variables-python-jp)  
[^3]: [GitHub Desktopのドキュメント](https://docs.github.com/ja/desktop)  
[^4]: GitHub Desktopのドキュメント中の[README.mdの項](https://docs.github.com/ja/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)  
[^5]: [記事の書き方](https://gist.github.com/LambdaNote/0d33b7d8284a3c99cffd1a5aa83c115f)
[^6]: commitとかに含めないファイルやフォルダを指定するやつ。  
[^7]: 書き方は[.gitignore の書き方](https://qiita.com/inabe49/items/16ee3d9d1ce68daa9fff)とか[[Git] .gitignoreの仕様詳解](https://qiita.com/anqooqie/items/110957797b3d5280c44f)とかに。  
[^8]: [python-dotenv公式ドキュメント](https://pypi.org/project/python-dotenv/)
[spotify-dashboard]: https://developer.spotify.com/dashboard/
