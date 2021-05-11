import argparse
import sys
import time
import numpy as np

def np_to_set(figure):
    set_figure = set()
    for cell in figure:
        set_figure.add((cell[0,0], cell[0,1]))
    return set_figure

class Orientation:
    def __init__(self):
        self.rotate90_matrix = np.matrix([[0, -1], [1, 0]])
        self.rotate180_matrix = np.matrix([[-1, 0], [0, -1]])
        self.rotate270_matrix = np.matrix([[0, 1], [-1, 0]])
        self.shift_x = 0
        self.shift_y = 0
        self.shift_matrix = np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    def rotate90(self, figure, axis_x = 0, axis_y = 0):
        tmp = self.shift(figure, -axis_x, -axis_y)
        tmp = tmp * self.rotate90_matrix
        return self.shift(tmp, axis_x, axis_y)


    def rotate180(self, figure, axis_x = 0, axis_y = 0):
        tmp = self.shift(figure, -axis_x, -axis_y)
        tmp = tmp * self.rotate180_matrix
        return self.shift(tmp, axis_x, axis_y)

    def rotate270(self, figure, axis_x = 0, axis_y = 0):
        tmp = self.shift(figure, -axis_x, -axis_y)
        tmp = tmp * self.rotate270_matrix
        return self.shift(tmp, axis_x, axis_y)

    def shift(self, figure, shift_x = 0, shift_y = 0):
        self.shift_matrix[2,0] = shift_x
        self.shift_matrix[2, 1] = shift_y
        ex_coord = np.column_stack((figure, np.array([1] * figure.shape[0])))
        return (ex_coord * self.shift_matrix)[:, :2]

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

def min_count(matrix, cols, k):
    min = 1000000000
    n_min = 0
    for col in cols:
        count = np.count_nonzero(matrix.transpose()[col] == k)
        if count < min:
            min = count
            n_min = col
    return n_min

def delete_rows(_set, ind_fig, row):
    i = 0
    while row <= ind_fig[i] or row > ind_fig[i+1]:
        i+=1
    for j in range(ind_fig[i], ind_fig[i+1]):
        if j in _set:
            _set.remove(j)

def solve(adj_matrix, ind_fig):
    adj_matrix = np.array(adj_matrix)
    solutions = []
    rows = set(i for i in range(adj_matrix.shape[0]))
    cols = set(i for i in range(adj_matrix.shape[1]))
    print("rows", rows)
    print("cols", cols)
    print("SOL", solutions)
    if not cols:
        print("Нет столбцов")
        return solutions
    min = 1000000000
    n_min = 0
    for col in cols:
        count = np.count_nonzero(adj_matrix.transpose()[col] == 1)
        if count < min and count > 0:
            min = count
            n_min = col
    c = n_min
    print("Мин столбец - ", c)
    if np.count_nonzero(adj_matrix.transpose()[c] == 1) == 0:
        print("Нет единиц в столбце")
        return solutions
    for row in set(rows):
        if adj_matrix[row][c] == 1:
            print("Строка с 1 - ", row)
            if row in set(rows):
                delete_rows(rows, ind_fig, row)
                solutions.append(row)
            step2(adj_matrix, rows, cols, row, solutions)
    return solutions


def step1(adj_matrix, rows, cols, solutions):
    print("rows", rows)
    print("cols", cols)
    print("SOL", solutions)
    if not cols:
        print("Нет столбцов")
        return solutions
    if not rows:
        print("Нет строк")
        return solutions
    c = min_count(adj_matrix, cols, 1)
    print("Мин столбец - ", c)
    if np.count_nonzero(adj_matrix.transpose()[c] == 1) == 0:
        print("Нет единиц в столбце")
        return solutions
    for row in set(rows):
        if row in rows:
            if adj_matrix[row][c] == 1:
                print("Строка с 1 - ", row)
                delete_rows(rows, ind_fig, row)
                solutions.append(row)
            step2(adj_matrix, rows, cols, row, solutions)

def step2(matrix, rows, cols, i, solutions):
    for j in set(cols):
        if matrix[i][j] == 1:
            cols.remove(j)
            for k in set(rows):
                if matrix[k][j] == 1:
                    rows.remove(k)
    step1(matrix, rows, cols, solutions)


def rectangle(S1, S2):
    matr = []
    for i in range(S1):
        for j in range(S2):
            matr.append([i, j])
    return np.matrix(matr)

def L_polyomino(Q1, Q2):
    matr = []
    for i in range(Q1):
        matr.append([i, 0])
    for j in range(1, Q2):
        matr.append([0, j])
    return np.matrix(matr)

print("Введите размер прямоугольника - стола в формате N M - ")
N, M = map(int, input().split())
# N = 5
# M = 3
board = Board(N, M)
print("Введите лист из тапл-пар в формате S1 S2 N S1 S2 N .... - ")
tapl_list = list(map(int, input().split()))
for i in range(len(tapl_list)//3):
    for j in range(tapl_list[i+2]):
        tapl_list.append([rectangle(tapl_list[i], tapl_list[i+1])])
adj = np.matrix([])
for fig in tapl_list:
    print("!!!", fig)
    adj = np.concatenate(adj, board.adjancy_matrix(fig))

print("Введите лист из тапл-пар в формате Q1 Q2 N Q1 Q2 N .... - ")
L_list = list(map(int, input().split()))
for i in range(len(L_list)//3):
    for j in range(L_list[i+2]):
        L_list.append([rectangle(L_list[i], L_list[i+1])])
for fig in L_list:
    adj = np.concatenate(adj, board.adjancy_matrix(fig))


print(adj)
if(solve(adj, [])):
    print("Правда")
else:
    print("Ложь")

# adj_matrix = np.concatenate((adj_matrix[6], adj_matrix[34]), axis = 0)
# board.adjancy_matrix_to_board(np.array(adj_matrix))