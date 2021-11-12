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

折角なのでGitHubを使う。GitHub Desktopを起動して（リモート？）リポジトリを作成。選択したローカルフォルダ直下に指定したリポジトリ名（今回はSpotifyApp）のフォルダができるらしい。README.mdはつけて `.gitignore` もPythonを選択。ライセンスはまあ後でええやろ。

AnacondaでPython3.8の新しい仮想環境を作り、Anaconda Promptで `pip install spotipy --upgrade` 。Spotipyの公式ドキュメントは[ここ](https://spotipy.readthedocs.io/en/2.19.0/)。また環境変数を使うために、[これ](https://www.twilio.com/blog/environment-variables-python-jp)を参考に `pip install python-dotenv` もしとく。

でなんかGitHub Desktop側でリポジトリフォルダをVS Codeで開くみたいなのがあったのでそれで作業を行う。都度 `README.md` にやったことをメモしていく。

また、後々 `Client ID` とか `Client Secret` とかをコード内で使うことになるが、そのままコードに組み込んでGitHubとかで公開するとマズいので、

`caitsith.py` とか名前は何でもいいので `.py` ファイルを作成する。なお左下の `Python x.x.xx 64-bit ('hogehoge': conda)` の箇所をクリックすれば仮想環境を選択できる。で `print ("Hello, Python!")` でもしてF5を押すとDebug Configurationとやらが出てくるが、そのままEnterを押せば `Python File` として実行してくれそう。[^1]


[^1]: ajajajajaja
