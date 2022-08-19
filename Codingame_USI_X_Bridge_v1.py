from snail_reversi.Board import BLACK, WHITE, DRAW
from snail_reversi.Board import Board

from USI_X_Engine_base_v1 import USIX_Engine_base as base

import subprocess as subpro
import time

#codingameのやつ
empty = '.' #空きマス
black_stone = '0'#黒石
white_stone = '1'#白石

#USI-X Othelloのやつ
USIX_empty = '-'#空きマス
USIX_black_stone = 'X'#黒石
USIX_white_stone = 'O'#白石

#改行
k = '\n'

class codingame_USI_X_Bridge(base):
    def __init__(self, path, name=None):
        super().__init__()
        self.engine_path = path
        self.name = name
        if name == None:
            self.name = path

    def load_engine(self):
        #起動
        self.engine = subpro.Popen(self.engine_path, stdin=subpro.PIPE, stdout=subpro.PIPE,
                                   universal_newlines=True, bufsize=1)
        #idとboard_sizeを送ったかを記録する変数
        self.send_id_and_boardsize = False
        return

    def send(self, command):
        #コマンド送信用
        if k not in command:
            command += k
            pass
        self.engine.stdin.write(command)
        return

    def recv(self):
        #コマンド受信用
        return self.engine.stdout.readline()

    def send_board(self):
        #Boardを送る
        if not self.send_id_and_boardsize:
            #まだ送ってないなら、idとboard_sizeを送る
            self.send({True: '0', False: '1'}[self.board.turn == BLACK])
            self.send('8')
            self.send_id_and_boardsize = True
        sfen = self.board.return_sfen()
        sfen = sfen[0:64].replace(USIX_empty,empty).replace(USIX_black_stone,
                                            black_stone).replace(USIX_white_stone, white_stone)
        lines = [sfen[0:8], sfen[8:16], sfen[16:24], sfen[24:32], sfen[32:40], sfen[40:48], sfen[48:56], sfen[56:64]]
        for i in range(len(lines)):
            self.send(lines[i])
        return

    def send_action(self):
        #legal_movesを送信
        legal_moves = self.board.gen_legal_moves()
        self.send(str(len(legal_moves)))
        for i in range(len(legal_moves)):
            self.send(legal_moves[i])
        return

    def set_board(self):
        #Bridge内部のBoardをセットする
        self.board = Board()
        if self.position_info['sfen'] != None:
            self.board.set_sfen(self.position_info['sfen'])
        for m in self.position_info['moves']:
            self.board.move_from_usix(m)
        self.send_board()
        return

    def isready(self, command):
        #isreadyの時にloadする
        self.load_engine()
        self.output('readyok')
        return

    def think(self):
        #思考本体
        self.send_action()
        """
        while True:
            move = self.recv()
            if len(move) >= 2:
                break
        """
        move = self.recv()
        bestmove = move[0] + move[1]
        return bestmove, None

if __name__ == '__main__':
    #この変数には、batファイルのPathを入れる
    ai_bat_file = 'test_codingameAI_1.bat'
    ai = codingame_USI_X_Bridge(ai_bat_file)
    ai.run()
