"""
Copyright (c) 2022 YuaHyodo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
元リポジトリへのリンク: https://github.com/YuaHyodo/USI-X_Othello_Samples
"""

from snail_reversi.Board import BLACK, WHITE, DRAW, PASS
from snail_reversi.Board import Board

from USI_X_Engine_base_v1 import USIX_Engine_base as base
import subprocess
import random
import time

k = '\n'

class Eval:
    """
    これを使えば様々な評価関数を使える様になる
    評価関数はbatファイルにでもしておけばたぶん動く
    サンプルの評価関数を用意しているので、そちらを見ながら作ってほしい

    プロトコルは単純
    isreadyと来たら、readyokと返し、

    eval [sfen]ときたら、
    score [score]で評価値を返す
    [sfen]には評価対象のsfenが、[score]には評価値が入る
    (scoreは、Pythonのfloatで変換できる型でなければならない)

    quitときたら停止する
    """
    def __init__(self, path):
        self.model = subprocess.Popen(path, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      universal_newlines=True, bufsize=1)
        self.send('isready')
        self.recv_word('readyok')

    def send(self, command):
        #コマンド送信用
        if k not in command:
            command += k
            pass
        self.model.stdin.write(command)
        return

    def recv(self):
        #コマンド受信用
        return self.model.stdout.readline()

    def recv_word(self, word):
        while True:
            message = self.recv()
            if word in message:
                break
        return message

    def main(self, sfen):
        self.send('eval ' + sfen)
        message = self.recv_word('score').split(' ')
        score = float(message[1])
        return score

class MiniMax(base):
    def __init__(self, path):
        super().__init__()
        self.name = ''
        self.auther = ''
        self.max_depth = 4#何手先を読むかの数字。大きいほど強いけど思考にその分に時間がかかる
        self.Max = 10000# +無限の代わり
        self.Min = self.Max * -1# -無限の代わり
        self.Draw_score = 0#引き分けの価値

        self.eval = Eval(path)#評価関数読み込み

        self.ordering_moves = {}

    def set_board(self):
        self.board = Board()
        if self.position_info['sfen'] != None:
            self.board.set_sfen(self.position_info['sfen'])
        for m in self.position_info['moves']:
            self.board.move_from_usix(m)
        return

    def score_color_change(self, score):
        #スコアの視点を変える
        return score * -1

    def AB_change(self, AB):
        return [-AB[1], -AB[0]]

    def Ordering(self):
        sfen = self.board.return_sfen()
        if sfen in self.ordering_moves.keys():
            return self.ordering_moves[sfen]
        legal_moves = self.board.gen_legal_moves()
        scores = {}
        for i in range(len(legal_moves)):
            self.board.move_from_usix(legal_moves[i])
            scores[legal_moves[i]] = self.eval.main(self.board.return_sfen())
            self.board.set_sfen(sfen)
        move_and_score = sorted(scores.items(), reverse=False, key=lambda x: x[1])
        moves = []
        for move in move_and_score:
            moves.append(move[0])
        self.ordering_moves[sfen] = moves
        return moves

    def minimax(self, depth, AB):
        #ゲームが終わったか？
        if self.board.is_gameover():
            #ゲームが終わったので、どっちが勝ったか調べる
            winner = self.board.return_winner()
            #手番側と非手番側のどっちが勝ったか調べる
            if winner == self.board.turn:
                return self.Max#手番側が勝った
            return self.Min#手番側が負けた
        
        if depth <= 0:#評価関数を呼ぶところに来たか？
            return self.eval.main(self.board.return_sfen())#評価関数を呼ぶ

        #まだ深く調べる必要がある

        #盤面を戻すための準備
        sfen = self.board.return_sfen()
        #次調べる手を準備する
        legal_moves = self.board.gen_legal_moves()
        #最高のスコアを保存しておく変数の準備
        bestscore = self.Min

        if PASS in legal_moves:
            self.board.move_from_usix(PASS)
            score = self.minimax(depth - 1, AB)
            self.board.set_sfen(sfen)
            return score
        
        #すべての手を調べる
        for move in legal_moves:
            self.board.move_from_usix(move)#打つ
            score = self.minimax(depth - 1, self.AB_change(AB))#調べる
            score = self.score_color_change(score)#手番側の視点に変える
            self.board.set_sfen(sfen)#戻す

            if score >= AB[1]:
                return score

            #最高スコアを更新したか？
            if score >= bestscore:
                #更新した
                bestscore = score
            AB[0] = max((AB[0], score))
            
        #全て調べた後の最高スコアを返す
        return bestscore

    def think(self):
        #盤面を復元する必要があるけど、snail_reversiには「1手戻る」機能がないのでsfenを使って無理やり戻す
        sfen = self.board.return_sfen()
        #次の手を取得
        legal_moves = self.Ordering()
        bestmove = None
        bestscore = self.Min
        AB = [self.Min, self.Max]
        
        if PASS in legal_moves:
            return PASS, None

        #すべての手を調べる
        for move in legal_moves:
            self.board.move_from_usix(move)#打つ
            score = self.minimax(self.max_depth - 1, self.AB_change(AB))#調べる
            score = self.score_color_change(score)#自分視点にする
            self.board.set_sfen(sfen)#戻す

            #今までで1番良い手か？
            if score >= bestscore:
                #良い手だったので更新
                bestmove = move
                bestscore = score
            AB[0] = max((AB[0], score))
        #1番良い手(最善手)を返す
        return bestmove, None

if __name__ == '__main__':
    path = 'Square_Weight_Eval_v1.bat'
    minimax_player = MiniMax(path)
    minimax_player.run()
