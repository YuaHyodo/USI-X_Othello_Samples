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

"""
こちらのコンテンツのサンプルコードhttps://github.com/YuaHyodo/USI-X-protocol_othello_version/blob/main/USI-X%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%B3%E3%81%AE%E4%BD%9C%E3%82%8A%E6%96%B9.md
"""

from snail_reversi.Board import BLACK, WHITE, DRAW
from snail_reversi.Board import Board

from USI_X_Engine_base_v1 import USIX_Engine_base as base
import random

class Player(base):
    def __init__(self):
        super().__init__()
        self.name = ''#エンジンの名前(なんでもいい)
        self.auther = ''#開発者の名前(なんでもいい)

    def set_board(self):
        #この関数では、エンジンの脳内盤をセットする
        self.board = Board()
        if self.position_info['sfen'] != None:
            self.board.set_sfen(self.position_info['sfen'])
        for m in self.position_info['moves']:
            self.board.move_from_usix(m)
        return

    def think(self):
        #この関数で思考する
        #ここを改造するだけで自分好みのAIが作れて、関連ツールの恩恵も受けられる。
        legal_moves = self.board.gen_legal_moves()#打てる場所のlistを受け取る
        bestmove = random.choice(legal_moves)#random.choiceで、ランダムに1つ手を選ぶ。
        return bestmove, None#2番目はPonderという機能だが、これは使わない。使わないときはNoneにする

if __name__ == '__main__':
    player = Player()
    player.run()#起動
