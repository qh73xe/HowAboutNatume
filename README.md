# HowAboutNatume

夏目漱石に質問をするための API (Action on Google の勉強のために作成)
ここでは API のみを管理.


## What is this.

- 夏目漱石が，種々の質問に答える API を作成
- 入力はなるべく自然言語に近づけるよう, 名詞, 形容詞，動詞のみを抽出.
- 解答は入力された語に対する similarity が最も高い名詞上位 3 件.


## How to do.

- 青空文庫から夏目漱石の文章をすべて抽出
- それぞれの文章を, 名詞，動詞, 形容詞のみのリストに変換
    - 形態素解析には mecab を使用.
- gemsim/word2vec を使い, 単語ネットを作成
- これを API から呼び出す.


## 動作イメージ

- user: ok google 夏目さんレコードと話す.
- bot: 夏目漱石のレコードに接続します．
- bot: 夏目漱石に質問をしてみてください.
- bot: 例えば, 「夏目先生, 人生って何」など.
- user: 夏目先生，人生って何
- bot: うーん, それはね. 「XX や XX, XX のことだよ」


## やりたいこと

1. 上記例で以下のやり取りを可能にする.
    - user: 夏目先生，どういうこと？
    - bot: 例えば私は XXX という本を書きました．
    - bot: よんでみてください.
    - bot: アンドロイド側に 青空文庫の URL を表示.


