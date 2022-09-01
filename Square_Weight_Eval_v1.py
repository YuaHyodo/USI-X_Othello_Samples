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
from Eval_base_v1 import Eval_base as base

from snail_reversi.Board import BLACK, WHITE, DRAW
from snail_reversi.Board import Board

import pickle as pk
import random
import math
import os

class Square_Weight_Eval(base):
    def __init__(self):
        super().__init__()
        self.model_file = './models/Square_Weight_Eval_v1_model.bin'
        self.board = Board()
        self.LR = 0.0001
        self.features_dict = {}
        self.scores_dict = {}

    def make_new_param(self):
        #パラメータは: 64マス分の重み + バイアスの65個
        weight = [0] * 64
        bias = 0
        self.param = [weight, bias]
        return

    def save(self):
        with open(self.model_file, 'wb') as f:
            pk.dump(self.param, f)
        return

    def load(self):
        with open(self.model_file, 'rb') as f:
            self.param = pk.load(f)
        return

    def input_feature(self, sfen=None):
        if sfen == None:
            sfen = self.board.return_sfen()
        if sfen in self.features_dict.keys():
            return self.features_dict[sfen]
        output = [0] * 64
        stones = self.board.make_simple_feature()
        for i in range(8):
            for j in range(8):
                output[i * 8 + j] = (stones[0][i][j] - stones[1][i][j])
        self.features_dict[sfen] = output
        return output

    def activation(self, inputs):
        return math.tanh(inputs)

    def activation_D(self, inputs):
        return 4.0 / ((math.exp(inputs) + math.exp(-inputs)) ** 2)

    def predict(self, inputs):
        output = 0
        for i in range(len(inputs)):
            output += (inputs[i] * self.param[0][i])
        output -= self.param[1]
        return self.activation(output)

    def set_board(self, sfen):
        self.board.set_sfen(sfen)
        return

    def Eval(self):
        sfen = self.board.return_sfen()
        if sfen in self.scores_dict.keys():
            return self.scores_dict[sfen]
        score = self.predict(self.input_feature())
        self.scores_dict[sfen] = score
        return score
    
    def train(self, data, epochs):
        files = os.listdir(data)
        files = [i for i in files if '.bin' in i]
        self.sfen_list = []
        for i in range(len(files)):
            with open(data + files[i], 'rb') as f:
                self.sfen_list.extend(pk.load(f))
        d = {'B': 1, 'W': -1, 'D': 0}
        self.dataset = []
        illegal_moves_count = 0
        for data in self.sfen_list:
            sfen = data['sfen']
            self.board.set_sfen(sfen)
            if ('bestmove' in data.keys()) and (data['bestmove'] not in self.board.gen_legal_moves()):
                illegal_moves_count += 1
            else:
                winner = d[data['winner']]
                turn_of = d[sfen[64]]
                self.dataset.append([self.input_feature(sfen=sfen), winner * turn_of])
        print('dataset_length:', len(self.dataset))
        print('illegal_moves_count:', illegal_moves_count)
        random.shuffle(self.dataset)
        
        self.test_dataset = self.dataset[0:100]#テストデータを用意する
        self.dataset = self.dataset[100:]#テストデータは訓練には使わない

        self.make_new_param()
        loss_graph = [0] * epochs
        loss_graph_test = [0] * epochs
        for epoch in range(epochs):
            print('train:', epoch, '|', epochs)
            for i in range(len(self.dataset)):
                v = self.predict(self.dataset[i][0])
                loss = self.dataset[i][1] - v
                delta = loss * self.activation_D(v)
                for j in range(64):
                    self.param[0][j] += (self.LR * self.dataset[i][0][j] * delta)
                self.param[1] += (self.LR * delta * -1)
                loss_graph[epoch] += abs(loss)
            loss_graph[epoch] /= len(self.dataset)
            for i in range(len(self.test_dataset)):
                loss_graph_test[epoch] += abs(self.dataset[i][1] - self.predict(self.test_dataset[i][0]))
            loss_graph_test[epoch] /= len(self.test_dataset)
        self.save()
        return loss_graph, loss_graph_test

#テスト用: eval O-XOOX---OO-OO--OOOXXXX-OOOXXXX-OOXOX-XOOXOXOXXOXXXOOOX-----OX--W1 
if __name__ == '__main__':
    Eval = Square_Weight_Eval()
    cmd = input()
    if cmd == 'train':
        dire = input('directory:')
        data1, data2 = Eval.train(dire, 10)
        import matplotlib.pyplot as plt
        plt.plot(data1, label='loss')
        plt.plot(data2, label='test_loss')
        plt.legend(loc='best')
        plt.show()
        print(Eval.param)
    else:
        Eval.load()
        Eval.output('readyok')
        Eval.run()
