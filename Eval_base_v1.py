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

class Eval_base:
    """
    評価関数の土台
    """
    def __init__(self):
        #初期化
        pass

    def load(self):
        #読み込みをする
        pass

    def output(self, command):
        #出力
        print(command, flush=True)
        return

    def Eval(self):
        #実際の計算を行う
        pass

    def set_board(self, sfen):
        #sfenからBoardをセットする
        pass

    def set_position(self, message):
        #メッセージからsfenを取り出し、それをset_boardに渡す
        message = message.split(' ')
        sfen = message[1]
        self.set_board(sfen)
        return

    def run(self):
        #メインループ
        while True:
            command = input()
            if command == 'isready':
                self.output('readyok')
            if 'eval' in command:
                self.set_position(command)
                score = self.Eval()
                self.output('score ' + str(score))
            if 'quit' in command:
                break
        return
            
