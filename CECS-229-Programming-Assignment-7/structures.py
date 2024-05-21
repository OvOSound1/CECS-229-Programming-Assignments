import math
from copy import deepcopy

class Vec:
    def __init__(self, contents=[]):
        self.elements = contents

    def __abs__(self):
        return math.sqrt(sum(e ** 2 for e in self.elements))

    def __add__(self, other):
        if len(self.elements) != len(other.elements):
            raise ValueError("Vectors must be the same length")
        return Vec([self.elements[i] + other.elements[i] for i in range(len(self.elements))])

    def __sub__(self, other):
        if len(self.elements) != len(other.elements):
            raise ValueError("Vectors must be the same length")
        return Vec([self.elements[i] - other.elements[i] for i in range(len(self.elements))])

    def __mul__(self, other):
        if isinstance(other, Vec):
            if len(self.elements) != len(other.elements):
                raise ValueError("Vectors must be the same length")
            return sum(self.elements[i] * other.elements[i] for i in range(len(self.elements)))
        elif isinstance(other, (float, int, complex)):
            return Vec([other * e for e in self.elements])
        else:
            raise ValueError("Unsupported operand type")

    def __rmul__(self, other):
        if isinstance(other, (float, int, complex)):
            return Vec([other * e for e in self.elements])
        else:
            raise ValueError("Unsupported operand type")

    def __truediv__(self, other):
        if isinstance(other, (float, int, complex)):
            return Vec([e / other for e in self.elements])
        else:
            raise ValueError("Unsupported operand type")

    def __len__(self):
        return len(self.elements)

    def __eq__(self, other):
        if not isinstance(other, Vec):
            raise TypeError(f"Cannot compare Vec with {type(other)}")
        return all(round(a, 4) == round(b, 4) for a, b in zip(self.elements, other.elements))

    def __getitem__(self, i):
        return self.elements[i]

    def __iter__(self):
        return iter(self.elements)

    def __hash__(self):
        return hash(tuple(self.elements))

    def __str__(self):
        return str(self.elements)


class Matrix:
    def __init__(self, rows):
        self.rows = rows
        self._construct_cols()

    def _construct_cols(self):
        self.cols = [list(col) for col in zip(*self.rows)]

    def _construct_rows(self):
        self.rows = [list(row) for row in zip(*self.cols)]

    def set_row(self, i, new_row):
        if len(new_row) != len(self.rows[0]):
            raise ValueError("New row must be of the same length as current rows")
        self.rows[i - 1] = new_row
        self._construct_cols()

    def set_col(self, j, new_col):
        if len(new_col) != len(self.cols[0]):
            raise ValueError("New column must be of the same length as current columns")
        self.cols[j - 1] = new_col
        self._construct_rows()

    def set_entry(self, i, j, val):
        self.rows[i - 1][j - 1] = val
        self._construct_cols()

    def get_row(self, i):
        return self.rows[i - 1]

    def get_col(self, j):
        return self.cols[j - 1]

    def get_entry(self, i, j):
        return self.rows[i - 1][j - 1]

    def get_columns(self):
        return self.cols

    def get_rows(self):
        return self.rows

    def get_diag(self, k):
        num_rows = len(self.rows)
        num_cols = len(self.cols)
        diag = []

        if k == 0:
            diag = [self.rows[i][i] for i in range(min(num_rows, num_cols))]
        elif k > 0:
            diag = [self.rows[i][i + k] for i in range(min(num_rows, num_cols - k))]
        elif k < 0:
            diag = [self.rows[i - k][i] for i in range(min(num_rows + k, num_cols))]

        return diag

    def __add__(self, other):
        if len(self.rows) != len(other.rows) or len(self.cols) != len(other.cols):
            raise ValueError("Matrices must have the same dimensions")
        return Matrix([[self.rows[i][j] + other.rows[i][j] for j in range(len(self.cols))] for i in range(len(self.rows))])

    def __sub__(self, other):
        if len(self.rows) != len(other.rows) or len(self.cols) != len(other.cols):
            raise ValueError("Matrices must have the same dimensions")
        return Matrix([[self.rows[i][j] - other.rows[i][j] for j in range(len(self.cols))] for i in range(len(self.rows))])

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            return Matrix([[self.rows[i][j] * other for j in range(len(self.cols))] for i in range(len(self.rows))])
        elif isinstance(other, Matrix):
            if len(self.cols) != len(other.rows):
                raise ValueError("Incompatible dimensions for matrix multiplication")
            return Matrix([[sum(self.rows[i][k] * other.rows[k][j] for k in range(len(self.cols))) for j in range(len(other.cols))] for i in range(len(self.rows))])
        elif isinstance(other, Vec):
            if len(self.cols) != len(other):
                raise ValueError("Incompatible dimensions for matrix-vector multiplication")
            return Vec([sum(self.rows[i][j] * other[j] for j in range(len(self.cols))) for i in range(len(self.rows))])
        else:
            raise TypeError(f"Matrix multiplication with {type(other)} is not supported")

    def __rmul__(self, other):
        if isinstance(other, (float, int)):
            return Matrix([[other * self.rows[i][j] for j in range(len(self.cols))] for i in range(len(self.rows))])
        else:
            raise TypeError(f"{type(other)} * Matrix is not supported")

    def dim(self):
        return len(self.rows), len(self.cols)

    def transpose(self):
        return Matrix(self.cols)

    def __str__(self):
        return '\n'.join(str(row) for row in self.rows)

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return False
        return all(
            round(self.rows[i][j], 3) == round(other.rows[i][j], 3)
            for i in range(len(self.rows)) for j in range(len(self.cols))
        )

    def __req__(self, other):
        return self.__eq__(other)