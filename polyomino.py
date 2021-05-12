import numpy as np
from Board import Board


def np_to_set(figure):
    set_figure = set()
    for cell in figure:
        set_figure.add((cell[0, 0], cell[0, 1]))
    return set_figure


def min_count(matrix, cols, k):
    min = 1000000000
    n_min = 0
    for col in cols:
        count = np.count_nonzero(matrix.transpose()[col] == k)
        if count < min:
            min = count
            n_min = col
    return n_min


def delete_rows(rows, ind_fig, row):
    i = 0
    while row > ind_fig["id" + str(i)]:
        i += 1
    if i != 0:
        for j in range(ind_fig["id" + str(i - 1)] + 1, ind_fig["id" + str(i)]):
            if j in rows:
                rows.remove(j)
    else:
        for j in range(ind_fig["id0"]):
            if j in rows:
                rows.remove(j)


def solve(adj_matrix, fig_dict):
    set_solutions = set()
    adj_matrix = np.array(adj_matrix)
    solutions = []
    rows = set(i for i in range(adj_matrix.shape[0]))
    cols = set(i for i in range(adj_matrix.shape[1]))
    if not cols:
        return solutions
    min = 1000000000
    n_min = 0
    for col in cols:
        count = np.count_nonzero(adj_matrix.transpose()[col] == 1)
        if count < min and count > 0:
            min = count
            n_min = col
    c = n_min
    if np.count_nonzero(adj_matrix.transpose()[c] == 1) == 0:
        return solutions
    for row in set(rows):
        if adj_matrix[row][c] == 1:
            if row in set(rows):
                delete_rows(rows, fig_dict, row)
                solutions.append(row)
            step2(adj_matrix, rows, cols, row, solutions, fig_dict)
    return solutions


def step1(adj_matrix, rows, cols, solutions, fig_dict):
    if not cols:
        return solutions
    if not rows:
        return solutions
    cols_used = set()
    cols_reserve = cols
    rows_reserve = rows
    while len(solutions) != len(fig_dict) and rows:
        cols_reserve, cols = cols, cols_reserve
        rows_reserve, rows = rows, rows_reserve
        c = min_count(adj_matrix, cols - cols_used, 1)
        cols_used.add(c)
        if np.count_nonzero(adj_matrix.transpose()[c] == 1) == 0:
            return solutions
        for row in set(rows):
            if adj_matrix[row][c] == 1:
                if row in set(rows):
                    delete_rows(rows, fig_dict, row)
                    solutions.append(row)
                step2(adj_matrix, rows, cols, row, solutions, fig_dict)
    return solutions


def step2(matrix, rows, cols, i, solutions, fig_dict):
    for j in set(cols):
        if matrix[i][j] == 1:
            cols.remove(j)
            for k in set(rows):
                if matrix[k][j] == 1:
                    if k in rows:
                        rows.remove(k)
    step1(matrix, rows, cols, solutions, fig_dict)


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


def set_cover(N, M, figure_list):
    board = Board(N, M)
    adj = board.adjancy_matrix(figure_list[0])
    figure_list.remove(figure_list[0])
    fig_dict = {"id0": len(adj)}
    ind = 1
    for fig in figure_list:
        adj_new = board.adjancy_matrix(fig)
        adj = np.concatenate((adj, adj_new), axis=0)
        fig_dict["id" + str(ind)] = len(adj_new) + fig_dict["id" + str(ind - 1)]
        ind += 1

    adj_matr = np.matrix([[] for i in range(N * M)])
    solv = solve(adj, fig_dict)

    if (len(solv) == len(fig_dict.values())):
        print("Правда")
    else:
        print("Ложь")

    adj_matr = np.matrix([adj[solv[0]]])
    solv.remove(solv[0])
    for i in solv:
        adj_matr = np.append(adj_matr, [adj[i]], axis=0)

    board.adjancy_matrix_to_board(np.array(adj_matr))


N = 5
M = 3
figure_list = [rectangle(2, 2), L_polyomino(2, 2), L_polyomino(2, 2), L_polyomino(3, 2)]

# N = 3
# M = 3
# figure_list = [L_polyomino(2, 2), L_polyomino(2, 2)]

# N = 4
# M = 3
# figure_list = [rectangle(2, 2), L_polyomino(2, 2), L_polyomino(3, 2)]

set_cover(N, M, figure_list)
