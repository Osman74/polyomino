import numpy as np

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