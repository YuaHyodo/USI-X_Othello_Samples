
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

class USIX_Engine_base:
    """
    これを使ってUSI-Xエンジンを作ると便利
    """
    def __init__(self):
        #エンジンの名前
        self.name = 'USI-X_Engine_base'
        #開発者の名前
        self.auther = ''
        #評価値の形式
        self.scoretype = 'stones'
        #評価値の最小値
        self.score_min = -64
        #評価値の最大値
        self.score_max = 64
        #ponder関係の処理に必要な値
        self.no_ponderhit = True

    def parse_time(self, command):
        """
        go btime 1000 wtime 2000 binc 1000 winc 2000 byoyomi 1000
        のようなコマンドから、持ち時間に関する情報を抜き出して、time_settingに書き込む
        """
        self.time_setting = {'btime': 'inf', 'wtime': 'inf', 'byoyomi': 0, 'binc': 0, 'winc': 0}
        lines = command.split(' ')
        check_key = None
        check = False
        for i in range(len(lines)):
            if check:
                self.time_setting[check_key] = int(lines[i])
                check = False
            else:
                for k in self.time_setting.keys():
                    if k in lines[i]:
                        check_key = lines[i]
                        check = True
                        break
        return

    def set_board(self):
        #探索部内のboardとかをここでセット
        return

    def think(self):
        #思考部をここに書く
        return 'bestmove', 'pondermove'

    def usi(self, command):
        """
        usiコマンドに対する応答
        """
        self.output('id name ' + self.name)
        self.output('id auther ' + self.auther)
        self.output('usiok')
        return

    def isready(self, command):
        """
        isreadyコマンドに対する応答
        """
        self.output('readyok')
        return

    def usinewgame(self, command):
        """
        usinewgameコマンドに対する応答
        """
        pass

    def position(self, command):
        """
        position startpos moves a1 a2
        などのコマンドから、局面情報を抜き出して、position_infoに書き出す
        """
        self.position_info = {'sfen': None, 'moves': []}
        lines = command.split(' ')
        read_moves = False
        next_is_sfen = False
        for i in range(len(lines)):
            if next_is_sfen:
                self.position_info['sfen'] = lines[i]
                next_is_sfen = False
            elif read_moves:
                self.position_info['moves'].append(lines[i])
            elif lines[i] == 'startpos':
                self.position_info['sfen'] = '---------------------------OX------XO---------------------------B1'
            elif lines[i] == 'sfen':
                next_is_sfen = True
            elif lines[i] == 'moves':
                read_moves = True
        self.set_board()
        return

    def go(self, command):
        """
        goコマンドが来た時に動く関数
        think関数が返すbestmoveやpondermoveをGUI側に伝えたりもする
        """
        if self.no_ponderhit:
            self.parse_time(command)
        bestmove, ponder = self.think()
        if ponder == None:
            message = 'bestmove ' + bestmove
        else:
            message = 'bestmove ' + bestmove + ' ponder ' + ponder
        self.output(message)
        self.no_ponderhit = True
        return

    def score_scale_and_type(self, command):
        """
        score_scale_and_typeコマンドが来たときに実行される
        """
        self.output('scoretype ' + self.scoretype + ' min ' + str(self.score_min) + ' max ' + str(self.score_max))
        return

    def ponder_hit(self, command):
        """
        ponderhitコマンドが来た時に実行される
        """
        self.parse_time(command)
        self.no_ponderhit = False
        return

    def stop(self):
        """
        stopコマンドが来た時に実行される
        """
        pass

    def quit(self):
        """
        quitコマンドが来たとき = 終了時に実行される
        """
        pass

    def output(self, message):
        """
        出力用の関数
        ログをとる機能を付けるのを容易にするためにこのようにしてみた。
        """
        print(message, flush=True)
        return

    def run(self):
        """
        メイン部
        ちょっと変わった実装方法になっている
        """
        self.command_dict = {'usi': self.usi, 'isready': self.isready, 'usinewgame': self.usinewgame,
                                         'position': self.position, 'go': self.go, 'score_scale_and_type': self.score_scale_and_type}
        while True:
            #コマンドが来るのを待機
            command = input()
            #コマンドが来たらそれに対応する関数を実行する
            if command in self.command_dict.keys():
                F = self.command_dict[command]
                F(command)
            elif command == 'quit':
                self.quit()
                break
            else:
                if command[0:2] in self.command_dict.keys():
                    F = self.command_dict[command[0:2]]
                    F(command)
                elif command[0:8] in self.command_dict.keys():
                    F = self.command_dict[command[0:8]]
                    F(command)
        return

if __name__ == '__main__':
    base = USIX_Engine_base()
    base.run()
