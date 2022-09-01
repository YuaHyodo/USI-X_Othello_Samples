# USI-X_Othello_Samples
USI-Xプロトコルに関するサンプルプログラムなどの置き場
# 概要
- ここはUSI-Xプロトコル(オセロ版)に関するサンプルプログラムの置き場。
- USI-Xプロトコル(オセロ版)についてはこちらを参照の事: https://github.com/YuaHyodo/USI-X-protocol_othello_version

# 各ファイル説明
## USI-X-Engine_base_v1.py
- USI-Xエンジンのベース
- これを利用してUSI-Xエンジンを作ると便利

## Codingame_USI_X_Bridge_v1.py
- codingame( https://www.codingame.com/multiplayer/bot-programming/othello-1 )のオセロAIをUSI-Xエンジンとして動かすツール(テスト不足)
- codingameのオセロAIを起動するbatファイルを用意すれば"多分"動く。(Pythonで作ったランダムプレーヤーでしか確認していない)
- 実行には、USI-X-Engine_base_v1.pyとsnail_reversi( https://github.com/YuaHyodo/snail_reversi )が必要。

## Step1.py, Step2.py
- こちらのリポジトリ( https://github.com/YuaHyodo/USI-X-protocol_othello_version )にある「USI-Xエンジンの作り方(初心者向け)」の第5章と6章のサンプルプログラム
- 実行には、USI-X-Engine_base_v1.pyとsnail_reversi( https://github.com/YuaHyodo/snail_reversi )が必要。

# ライセンス
- このリポジトリに置いてあるサンプルコードはMITライセンスです。
- 詳細はLICENSEファイルを確認してください。
