

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
            
