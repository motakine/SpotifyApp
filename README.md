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

# 作る手順メモ
まずSpotifyにログインし、Spotify for Developersの[Dashboard](https://developer.spotify.com/dashboard/login)にもSpotifyアカウントを使ってログインする。次に `CREATE AN APP` からアプリを作成する。  
なお `Client ID` と "SHOW CLIENT SECRET" クリックで表示される `Client Secret` は後で必要になる。晒すとヤバそう。

折角なのでGitHubを使う。GitHub Desktopを起動して（ローカル？）リポジトリを作成。選択したローカルフォルダ直下に指定したリポジトリ名（今回はSpotifyApp）のフォルダができるらしい。README.mdはつけて `.gitignore` もPythonを選択。ライセンスはまあ後でええやろ。

AnacondaでPython3.8の新しい仮想環境を作り、Anaconda Promptで `pip install spotipy --upgrade` [^1]。また環境変数を使うために `pip install python-dotenv` もしとく[^2]。

でなんかGitHub Desktop側でリポジトリフォルダをVS Codeで開くみたいなのがあったのでそれで作業を行う。都度 `README.md` にやったことをメモしていく。

また、後々 `Client ID` とか `Client Secret` とかをコード内で使うことになるが、そのままコードに組み込んでGitHubとかで公開するとマズいので、`.env`ファイル内に環境変数として記述しておき、コード内では`python-dotenv`の関数を使うことにする。  
但し`.env`ファイルをGitHubに公開してしまうとそれもマズいので、`.gitignore`に`.env`の行が含まれていることを確認する（リポジトリを作成するときの設定でデフォで入ってるはず）。必要な環境変数は[Spotify Web APIのクイックスタート](https://developer.spotify.com/documentation/web-api/quick-start/)を参照した。  
どんな環境変数を使っているかをGitHubに公開したい場合は`.env.example`ファイルを作成してそこに適当に書く（本物のキーを入力しないように）[^2]。

`caitsith.py` とか名前は何でもいいので `.py` ファイルを作成する。なお左下の `Python x.x.xx 64-bit ('hogehoge': conda)` の箇所をクリックすれば仮想環境を選択できる。で `print ("Hello, Python!")` でもしてF5を押すとDebug Configurationとやらが出てくるが、そのままEnterを押せば `Python File` として実行してくれそう。[^1]

## GitHubいろいろ
今回使用しているのはいつ入れたか忘れたGitHub Desktop[^3]。コマンドラインは嫌や！

File > New Repositoryしてからローカルフォルダ指定・README.md[^4][^5]・`.gitignore`[^6][^7]・ライセンスをなんやかんやしてリポジトリ作成。今後変更があった場合は適宜（ローカルリポジトリに）commitを行う。

なおこのままだと外部には公開されていないので、Publish repositoryでGitHubのサイトに公開する。このとき`Keep this code private`にチェックを入れたままだと他人が見られないので注意。後からサイトにアクセスしてSettingのDanger Zoneから公開設定を変更できるが赤くて怖いので注意。

以降ローカルの変更をcommitしたあとにリモートにも反映させる場合は、Publish repositoryがPush OriginになっているのでそこからPushができる。



[^1]: [Spotipy公式ドキュメント](https://spotipy.readthedocs.io/en/2.19.0/)  
[^2]: [twilio BLOG: Pythonで環境変数を活用する](https://www.twilio.com/blog/environment-variables-python-jp)  
[^3]: [GitHub Desktopのドキュメント](https://docs.github.com/ja/desktop)  
[^4]: GitHub Desktopのドキュメント中の[README.mdの項](https://docs.github.com/ja/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)  
[^5]: [記事の書き方](https://gist.github.com/LambdaNote/0d33b7d8284a3c99cffd1a5aa83c115f)
[^6]: commitとかに含めないファイルやフォルダを指定するやつ。  
[^7]: 書き方は[.gitignore の書き方](https://qiita.com/inabe49/items/16ee3d9d1ce68daa9fff)とか[[Git] .gitignoreの仕様詳解](https://qiita.com/anqooqie/items/110957797b3d5280c44f)とかに。
