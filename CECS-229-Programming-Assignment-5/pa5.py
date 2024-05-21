from Vec import Vec

"""-------------------- PROBLEM 1 --------------------"""
class Matrix:

    def __init__(self, rows):
        self.rows = rows
        self.cols = self._construct_cols()

    def get_rows(self):
        return self.rows

    def get_cols(self):
        return self.cols

    def set_rows(self, rows):
        self.rows = rows
        self.cols = self._construct_cols()

    def set_row(self, index, row):
        if index < 1 or index > len(self.rows):
            raise IndexError("Index out of range")
        if len(row) != len(self.rows[0]):
            raise ValueError("Row length must match current row length")
        self.rows[index-1] = row
        self.cols = self._construct_cols()

    def set_cols(self, j, new_col):
        for i in range(len(self.rows)):
            self.rows[i][j-1] = new_col[i]
        self.cols = self._construct_cols()

    def _construct_cols(self):
        return list(map(list, zip(*self.rows)))

    def _construct_rows(self):
        return list(map(list, zip(*self.cols)))
      
    def __add__(self, other):
        if isinstance(other, Matrix):
            if len(self.rows) != len(other.get_rows()) or len(self.rows[0]) != len(other.get_rows()[0]):
                raise ValueError("Matrices must have the same dimensions to add")
            return Matrix([[self.rows[i][j] + other.get_rows()[i][j] for j in range(len(self.rows[0]))] for i in range(len(self.rows))])
        else:
            raise TypeError("Unsupported operand type for +: 'Matrix' and '{}'".format(type(other)))

    def __sub__(self, other):
        if isinstance(other, Matrix):
            if len(self.rows) != len(other.get_rows()) or len(self.rows[0]) != len(other.get_rows()[0]):
                raise ValueError("Matrices must have the same dimensions to subtract")
            return Matrix([[self.rows[i][j] - other.get_rows()[i][j] for j in range(len(self.rows[0]))] for i in range(len(self.rows))])
        else:
            raise TypeError("Unsupported operand type for -: 'Matrix' and '{}'".format(type(other)))

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Matrix([[self.rows[i][j] * other for j in range(len(self.rows[0]))] for i in range(len(self.rows))])
        elif isinstance(other, Matrix):
            if len(self.rows[0]) != len(other.get_rows()):
                raise ValueError("The number of columns of the first matrix must be equal to the number of rows of the second matrix")
            return Matrix([[sum(a*b for a, b in zip(self.rows[i], col)) for col in other.get_cols()] for i in range(len(self.rows))])
        elif isinstance(other, Vec):
            if len(self.rows[0]) != len(other):
                raise ValueError("The number of columns of the matrix must be equal to the number of elements in the vector")
            return Vec([sum(a*b for a, b in zip(self.rows[i], other)) for i in range(len(self.rows))])
        else:
            raise TypeError("Unsupported operand type for *: 'Matrix' and '{}'".format(type(other)))

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return self * other
        else:
            raise TypeError("Unsupported operand type for *: '{}' and 'Matrix'".format(type(other)))

    def get_entry(self, i, j):
      return self.rows[i-1][j-1]

    def get_diag(self, k):
        m, n = len(self.rows), len(self.rows[0])
        if k >= 0:
          return [self.rows[i][i+k] for i in range(min(m, n-k)) if i+k < n]
        else:
          k = -k
          return [self.rows[i+k][i] for i in range(min(m-k, n)) if i+k < m]

    def set_entry(self, i, j, val):
        self.rows[i-1][j-1] = val
        self.cols = self._construct_cols()

    def get_row(self, i):
        return self.rows[i-1]

    def get_col(self, j):
        return self.cols[j-1]

    def get_columns(self):
        return self.cols

    def set_col(self, j, new_col):
        if len(new_col) != len(self.rows):
            raise ValueError("New column length must match current number of rows")
        for i in range(len(self.rows)):
            self.rows[i][j-1] = new_col[i]
        self.cols = self._construct_cols()


    '''-------- ALL METHODS BELOW THIS LINE ARE FULLY IMPLEMENTED -------'''

    def dim(self):
        """
        gets the dimensions of the mxn matrix
        where m = number of rows, n = number of columns
        :return: tuple type; (m, n)
        """
        m = len(self.rows)
        n = len(self.cols)
        return (m, n)

    def __str__(self):
        """prints the rows and columns in matrix form """
        mat_str = ""
        for row in self.rows:
            mat_str += str(row) + "\n"
        return mat_str

    def __eq__(self, other):
        """
        overloads the == operator to return True if
        two Matrix objects have the same row space and column space
        """
        if type(other) != Matrix:
            return False
        this_rows = [round(x, 3) for x in self.rows]
        other_rows = [round(x, 3) for x in other.rows]
        this_cols = [round(x, 3) for x in self.cols]
        other_cols = [round(x, 3) for x in other.cols]

        return this_rows == other_rows and this_cols == other_cols

    def __req__(self, other):
        """
        overloads the == operator to return True if
        two Matrix objects have the same row space and column space
        """
        if type(other) != Matrix:
            return False
        this_rows = [round(x, 3) for x in self.rows]
        other_rows = [round(x, 3) for x in other.rows]
        this_cols = [round(x, 3) for x in self.cols]
        other_cols = [round(x, 3) for x in other.cols]

        return this_rows == other_rows and this_cols == other_cols


"""-------------------- PROBLEM 2 --------------------"""

from math import cos, sin

def rotate_2Dvec(v: Vec, tau: float):
    """
    computes the 2D-vector that results from rotating the given vector
    by the given number of radians
    :param v: Vec type; the vector to rotate
    :param tau: float type; the radians to rotate by
    :return: Vec type; the rotated vector
    """
    x = v[0]*cos(tau) - v[1]*sin(tau)
    y = v[0]*sin(tau) + v[1]*cos(tau)
    return Vec([x, y])
