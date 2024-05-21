import math
from copy import deepcopy


class Vec:
    def __init__(self, contents=[]):
        """
        constructor defaults to empty vector
        accepts list of elements to initialize a vector object with the
        given list
        """
        self.elements = contents
        return

    def __abs__(self):
        """
        overloads the built-in function abs(v)
        :return: float type; the Euclidean norm of vector v
        """
        return math.sqrt(sum([e ** 2 for e in self.elements]))

    def __add__(self, other):
        """
        overloads the + operator to support Vec + Vec
        :raises: ValueError if vectors are not same length
        """
        if len(self.elements) == len(other.elements):
            return Vec([self.elements[i] + other.elements[i] for i in range(len(self.elements))])
        else:
            raise ValueError("ERROR: Vectors must be same length")

    def __mul__(self, other):
        """
        overloads the * operator to support
            - Vec * Vec (dot product) raises ValueError if vectors are not same length in the case of dot product
            - Vec * float (component-wise product)
            - Vec * int (component-wise product)
        :raises: ValueError if vectors are not of same length in Vec * Vec operation
        """
        if type(other) == Vec:  # define dot product
            if len(self.elements) == len(other.elements):
                return sum([self.elements[i] * other.elements[i] for i in range(len(self.elements))])
            else:
                raise ValueError("ERROR: Vectors must be same length")
        elif type(other) == float or type(other) == int:  # scalar-vector multiplication
            return Vec([other * self.elements[i] for i in range(len(self.elements))])

    def __rmul__(self, other):
        """
        overloads the * operator to support
            - float * Vec
            - int * Vec
        """
        if type(other) == float or type(other) == int:
            return Vec([other * self.elements[i] for i in range(len(self.elements))])
        else:
            raise ValueError("ERROR: Incompatible types.")

    def __str__(self):
        """returns string representation of this Vec object"""
        return str(self.elements)

    def __sub__(self, other):
        """
        overloads the - operator to support Vec - Vec
        :raises: ValueError if vectors are not same length
        """
        if type(other) == Vec and len(self.elements) == len(other.elements):
            return Vec([self.elements[i] - other.elements[i] for i in range(len(self.elements))])
        elif type(other) == Vec:
            raise ValueError("ERROR: Vectors must be same length")
        else:
            raise ValueError("ERROR: Incompatible types.")

    def __truediv__(self, other):
        if type(other) == float or type(other) == int:
            return Vec([self.elements[i] / other for i in range(len(self.elements))])
        else:
            raise ValueError("ERROR: Incompatible types.")

    def __len__(self):
        """
        overloads the len() function to support len(Vec)
        :return: int type; the number of elements in this Vec object
        """
        return len(self.elements)

    def __eq__(self, other):
        """
        overloads the == operator to support Vec == Vec
        :raises: TypeError if other is not Vec type
        :return: True if the elements of self rounded to four (4) decimal
                  places are the same as the elements of other rounded to
                  four (4) decimal places
        """
        if type(other) != Vec:
            raise TypeError(f"{self} == {other} is not defined")
        rounded_self = [round(x, 4) for x in self.elements]
        rounded_other = [round(x, 4) for x in other.elements]
        return rounded_other == rounded_self

    def __getitem__(self, i: int):
        """
        overloads the slicing operator [] to support Vec object slicing
        :param i: the index of the desired element
        :return: the object at index of i of this Vec object
        """
        return self.elements[i]

    def __iter__(self):
        """
        overloads the list() function so that list(Vec) returns
        the elements of the vector in a Python list
        :return: list type; the elements of the vector
        """
        return iter(self.elements)


# class Matrix:
#
#     def __init__(self, rows=[]):
#         """
#         initializes a Matrix with given rows
#         :param rows: the list of rows that this Matrix object has
#         """
#         self.rows = rows
#         self.cols = []
#         self._construct_cols()
#         return
#
#     # FIXME: Copy-paste the missing methods from your Matrix class from pa5.py here
#
#     def transpose(self):
#         """
#         returns the transpose of this matrix
#         :return: Matrix type; distinct Matrix object that represents the transpose of this matrix
#         """
#         rows = deepcopy(self.cols)
#         return Matrix(rows)

class Matrix:

    def __init__(self, rows):
        """
        initializes a Matrix with given rows
        :param rows: the list of rows that this Matrix object has
        """
        self.rows = rows
        self.cols = []
        self._construct_cols()
        self._construct_rows()
        return

    """
  INSERT MISSING SETTERS AND GETTERS HERE
  """

    #SETTER METHOD
    def set_row(self,i, new_row):
        if len(new_row) != len(self.rows[0]):
            raise ValueError

        for k in range(len(self.rows[0])):
            self.rows[i-1][k] = new_row[k]
        #print("my new row: ",self.rows)
        self._construct_cols()


    def set_col(self,j,new_col):

        if len(new_col) != len(self.cols[0]):
            raise ValueError
        for k in range(len(self.cols[0])):
            # print('old value: ', self.cols[k])
            self.cols[j - 1][k] = new_col[k]
        self._construct_rows()

    def set_entry(self,i,j,val):
        self.rows[i-1][j-1] = val
        self._construct_cols()
        self._construct_rows()


    #GETTER METHOD
    def get_row(self,i):
        return self.rows[i-1]

    def get_col(self,j):
        return self.cols[j-1]

    def get_entry(self,i,j):
        return self.rows[i-1][j-1]

    def get_columns(self):
        return self.cols

    def get_rows(self):
        return self.rows


    def get_diag(self,k):
        myList = []

        num_rows = len(self.rows)
        num_cols = len(self.cols)
        if k == 0:
            for i in range(min(num_rows,num_cols)):
                # print("time running: ",len(self.rows[0]) - k)
                # print("dig0 [i]: ",i)
                # print("my dig0 value: ",self.rows[i][i])
                myList.append(self.rows[i][i])

        if k >0:
            for i in range(min(num_rows,num_cols-k)):
                myList.append(self.rows[i][i+k])

        if k < 0:
            for i in range(min(num_rows+k,num_cols)):
                myList.append(self.rows[i-k][i])
        return myList

    def _construct_cols(self):
        """
        HELPER METHOD: Resets the columns according to the existing rows
        """
        self.cols = []
        # print("my self col: ",self.cols)
        # print("\n my len list0: ",len(self.rows[0]))
        # print("\n my len array: ",len(self.rows))

        num_Column = len(self.rows[0])

        for i in range(num_Column):
            innerList = []
            for j in self.rows:
                innerList.append(j[i])
            self.cols.append(innerList)

        # DONE: INSERT YOUR IMPLEMENTATION HERE

    def _construct_rows(self):
        """
        HELPER METHOD: Resets the rows according to the existing columns
        """
        num_Row = len(self.cols[0])
        self.rows = []
        # DONE: INSERT YOUR IMPLEMENTATION HERE

        for i in range(num_Row):
            innerList = []
            for j in self.cols:
                innerList.append(j[i])
            self.rows.append(innerList)

        print("my row1: ")
        print(self.rows)
        return

    def __add__(self, other):
        """
        overloads the + operator to support Matrix + Matrix
        :param other: the other Matrix object
        :raises: ValueError if the Matrix objects have mismatching dimensions
        :raises: TypeError if other is not of Matrix type
        :return: Matrix type; the Matrix object resulting from the Matrix + Matrix operation
        """
        #DONE: REPLACE WITH IMPLEMENTATION
        myList = []
        if len(self.rows) == len(other.rows) and len(self.cols) == len(other.cols):
            #implement the function
            for i in range(len(self.rows)):
                innerList = []
                for j in range(len(self.cols)):
                    innerList.append(self.rows[i][j]+other.rows[i][j])
                myList.append(innerList)
            return Matrix(myList)
        else:
            raise ValueError

    def __sub__(self, other):
        """
        overloads the - operator to support Matrix - Matrix
        :param other:
        :raises: ValueError if the Matrix objects have mismatching dimensions
        :raises: TypeError if other is not of Matrix type
        :return: Matrix type; the Matrix object resulting from Matrix - Matrix operation
        """
          # DONE: REPLACE WITH IMPLEMENTATION

        myList = []
        if len(self.rows) == len(other.rows) and len(self.cols) == len(other.cols):
            # implement the function
            for i in range(len(self.rows)):
                innerList = []
                for j in range(len(self.cols)):
                    innerList.append(self.rows[i][j] - other.rows[i][j])
                myList.append(innerList)
            return Matrix(myList)
        else:
            raise ValueError

    def __mul__(self, other):
        """
        overloads the * operator to support
            - Matrix * Matrix
            - Matrix * Vec
            - Matrix * float
            - Matrix * int
        :param other: the other Matrix object
        :raises: ValueError if the Matrix objects have mismatching dimensions
        :raises: TypeError if other is not of Matrix type
        :return: Matrix type; the Matrix object resulting from the Matrix + Matrix operation
        """

        myList = []
        if type(other) == float or type(other) == int:
            print("Insert implementation of MATRIX-SCALAR multiplication")
            print("other value scalar: ",other)
            # implement the function
            for i in range(len(self.rows)):
                innerList = []
                for j in range(len(self.cols)):
                    innerList.append(self.rows[i][j]*other)
                myList.append(innerList)


        elif type(other) == Matrix:
            print("Insert implementation of MATRIX-MATRIX multiplication")

            if len(self.cols) != len(other.rows):
                raise ValueError

            for i in range(len(self.rows)):
                innerList = []
                for j in range(len(other.cols)):
                    result = 0
                    for k in range(len(self.cols)):
                        result += self.rows[i][k] * other.rows[k][j]
                    innerList.append(result)

                myList.append(innerList)

        elif type(other) == Vec:
            print("Insert implementation for MATRIX-VECTOR multiplication")
            if len(self.cols) != len(other):
                raise ValueError
            for i in range(len(self.rows)):
                result = 0
                for j in range(len(self.cols)):
                    result += self.rows[i][j] * other[j]
                myList.append(result)

            return Vec(myList)

        else:
            raise TypeError(f"Matrix * {type(other)} is not supported.")

        return Matrix(myList)


    def __rmul__(self, other):
        """
        overloads the * operator to support
            - float * Matrix
            - int * Matrix
        :param other: the other Matrix object
        :raises: ValueError if the Matrix objects have mismatching dimensions
        :raises: TypeError if other is not of Matrix type
        :return: Matrix type; the Matrix object resulting from the Matrix + Matrix operation
        """
        myList = []
        if type(other) == float or type(other) == int:
            print("FIXME: Insert implementation of SCALAR-MATRIX multiplication"
                  )
            for i in range(len(self.rows)):
                innerList = []
                for j in range(len(self.cols)):
                    innerList.append(self.rows[i][j]*other)
                myList.append(innerList)
        else:
            raise TypeError(f"{type(other)} * Matrix is not supported.")
        return Matrix(myList)

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

    def transpose(self):
        """
        returns the transpose of this matrix
        :return: Matrix type; distinct Matrix object that represents the transpose of this matrix
        """
        rows = deepcopy(self.cols)
        return Matrix(rows)