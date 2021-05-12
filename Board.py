from Orientation import Orientation
import numpy as np

class Board:
    def __init__(self, N, M):
        self.N = N
        self.M = M
        self.figures = []
        self.orient = Orientation()

    def display(self):
        self.board = []
        for i in range(self.N):
            self.board.extend([0] * self.M)
        for i in range(self.M):
            print('|', end='')
            for j in range(self.N):
                print(self.board[i * self.M + j], end='|')
            print()

    def display_figure(self, figure):
        self.board = []
        for i in range(self.N):
            self.board.extend([0] * self.M)
        for cell in figure:
            i = self.N - cell[0, 1] - 1
            j = cell[0, 0]
            print(i, j)
            print(i * self.M + j)
            self.board[i * self.M + j] = "X"
        for i in range(self.N):
            print('|', end='')
            for j in range(self.M):
                print(self.board[i * self.M + j], end='|')
            print()
        print()

    def add_figure(self, figure):
        self.figures.append(figure)

    def pos_is_real(self, figure):
        for cell in figure:
            if cell[0,0] < 0 or cell[0,1] < 0 or cell[0,0] >= self.N or cell[0,1] >= self.M:
                return False
        return True

    def is_equivalent(self, figure_A, figure_B):
        return np_to_set(figure_A) == np_to_set(figure_B)

    def all_possible_shifts(self, figure, count, all_pos = []):
        for i in range(-np.max(figure[:, 0]),self.N - np.max(figure[:, 0])):
            for j in range(-np.max(figure[:, 1]), self.M - np.max(figure[:, 1])):
                shift_figure = self.orient.shift(figure, i, j)
                if self.pos_is_real(shift_figure):
                    # self.display_figure(shift_figure)
                    count += 1
                    all_pos.append(shift_figure)
        return count


    def all_positions(self, figure, square = False):
        all_pos = []
        rotate_figure = figure
        count = 0
        count = self.all_possible_shifts(rotate_figure, count, all_pos)
        if not square:
            rotate_figure = self.orient.rotate90(figure)
            count = self.all_possible_shifts(rotate_figure, count, all_pos)
            rotate_figure = self.orient.rotate180(figure)
            count = self.all_possible_shifts(rotate_figure, count, all_pos)
            rotate_figure = self.orient.rotate270(figure)
            count = self.all_possible_shifts(rotate_figure, count, all_pos)
        return all_pos

    def adjance_vector(self, figure):
        vec = [0 for i in range(self.N*self.M)]
        for cell in figure:
            i = cell[0, 0]
            j = cell[0, 1]
            vec[i * self.M + j] = 1
        return vec

    def adjancy_matrix(self, figure, square = False):
        all_pos = self.all_positions(figure, square)
        adj_matr = []
        for fig in all_pos:
            adj_matr.append(self.adjance_vector(fig))
        return adj_matr

    def adjancy_matrix_to_board(self, adj_matrix, names = "ABCDEFGH"):
        self.board = []
        for i in range(self.N):
            self.board.extend([0] * self.M)
        k = 0
        for figure in adj_matrix:
            j = 0
            for cell in figure:
                if cell:
                    self.board[j] = names[k]
                j += 1
            k += 1
        for i in range(self.N):
            print('|', end='')
            for j in range(self.M):
                print(self.board[i * self.M + j], end='|')
            print()
        print()