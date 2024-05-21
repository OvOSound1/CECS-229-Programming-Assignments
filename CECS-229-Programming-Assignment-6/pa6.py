  import copy
  from structures import Matrix, Vec
  import random
  import numpy as np
  import helpers
  """ ----------------- PROBLEM 1 ----------------- """


  def norm(v: Vec, p: int):
      """
      returns the p-norm of Vec v
      :param v: Vec type; the Vec object for which the norm will be applied
      :param p: int type; the integer determining the norm to be calculated
      :returns: float type; the norm as a float
      """
      # TODO: implement this function
      # print("my Vec: ",v)
      myResult = 0
      for i in v:
          myResult += abs(i)**(p)
      #and calculate root overall
      return myResult**(1/p)


  """ ----------------- PROBLEM 2 ----------------- """


  def _ref(A: Matrix):
      B = Matrix(copy.deepcopy(A.rows))
      m, n = B.dim()
      k = 1  # initializing the row-index of where to begin searching for the pivot
      for j in range(1, n + 1):
          p = _pivot_idx(k, j, B)  # gets the index of the pivot at column j
          if p is None:
              continue
          if p != k:  # we must swap row k with row p
              B.rows[k - 1], B.rows[p - 1] = B.rows[p - 1], B.rows[k - 1]  # swap rows
          pivot = B.get_entry(k, j)  # pivot at column j
          new_row = [entry / pivot for entry in B.get_row(k)]  # new row should be row k divided by the pivot
          print("new row: ", new_row)
          B.set_row(k, new_row)
          # reducing the rows below row k by a scalar multiple of row k
          for i in range(k + 1, m + 1):
              scalar = B.get_entry(i, j)
              reduced_row = [B.get_entry(i, col) - scalar * B.get_entry(k, col) for col in range(1, n + 1)]
              # Ensure that elements below the pivot are set to zero if they are very close to zero
              reduced_row = [0.0 if abs(entry) < 1e-10 else entry for entry in reduced_row]
              print("reduced row: ", reduced_row)  # Print the reduced row for debugging
              B.set_row(i, reduced_row)
          k += 1
      return B


  """ ----------------- PROBLEM 3 ----------------- """


  def rank(A: Matrix):
      """
      returns the rank of the given Matrix object
      as an integer

      Apply Gaussian Elimination
      """
      # B = Matrix(copy.deepcopy(A.rows))
      # m, n = B.dim()
      # return min(m,n)

      temp_matrix = _ref(A)
      ref_matrix = []
      row_num = 0
      num_rows = len(A.rows)

      while row_num < num_rows:
          curr_row = temp_matrix.get_row(row_num)
          ref_list = []

          for j in range(len(curr_row)):
              ref_list.append(curr_row[j])

          row_num += 1
          ref_matrix.append(ref_list)

      for i in range(len(ref_matrix)):
          for j in range(len(ref_matrix[i])):
              ref_matrix[i][j] = round(ref_matrix[i][j], 2)

      rank_counter = 0

      for i in range(len(ref_matrix)):
          non_zero_counter = 0
          for j in range(len(ref_matrix[0])):

              if j == len(ref_matrix[0]) - 1:  # check if last index is 0
                  # print("last index:", ref_matrix[i][j])
                  if ref_matrix[i][j] == 0 and non_zero_counter <= 1:
                      # print("this is not counted in rank")
                      non_zero_counter = 0  # set variable back to 0 to mark as linearly dependent
                  elif ref_matrix[i][j] != 0:
                      non_zero_counter += 1

              elif ref_matrix[i][j] != 0:
                  non_zero_counter += 1

          if non_zero_counter > 0:
              rank_counter += 1

      return rank_counter



  """ ----------------- PROBLEM 4 ----------------- """


  def gauss_solve(A: Matrix, b: Vec):
      """
      returns the Row Echelon Form of the Matrix A
      :param A: Matrix type
      :returns: Matrix type; distinct Matrix object that is the
                Row-Echelon Form of A
      """
      new_cols = copy.deepcopy(A.cols)
      new_cols.append(b.elements)

      Ag = Matrix(new_cols).transpose()
      Arank = rank(A)
      Agrank = rank(Ag)
      m, n = A.dim()

      if Arank != Agrank:  # No Solution
          return None
      elif Arank < n:  # Infinite Solutions
          num_free_variables = A.dim()[1] - Arank
          return num_free_variables
      else:  # Unique Solution
          # solve for unique solution
          len_matrix = len(A.rows)
          len_vec = len(b.elements)

          if len_matrix != len_vec:
              raise ValueError("dimensions do not match")
          else:
              # obtain rank of ref of matrix and ag matrix
              rank_ref_a = rank(A)

              # rank ag matrix
              ag_matrix = []
              for i in range(len_matrix):
                  row_list = []
                  for j in range(len(A.cols) + 1):
                      row_list.append(0)
                  ag_matrix.append(row_list)

              temp_matrix = []
              for i in range(len(A.rows)):
                  row_list = []
                  for j in range(len(A.cols)):
                      row_list.append(A.rows[i][j])
                  temp_matrix.append(row_list)

              vec_list = []
              for num in b.elements:
                  vec_list.append(num)

              for i in range(len_matrix):
                  for j in range(len(A.cols)):
                      ag_matrix[i][j] = temp_matrix[i][j]

              for i in range(len(vec_list)):
                  ag_matrix[i][len(ag_matrix[0]) - 1] = vec_list[i]

              #ref_ag = Matrix(ag_matrix).ref()
              ref_ag = _ref(Matrix(ag_matrix))
              rank_ag = rank(ref_ag)

              if rank_ref_a == rank_ag:
                  num_variables = len(temp_matrix[0])

                  if rank_ag < num_variables:
                      return Arank - Agrank
                  elif rank_ag == num_variables:
                      solution = []
                      for i in range(num_variables - 1, -1, -1):
                          if i == num_variables - 1:
                              x_i = ref_ag.rows[i][num_variables] / ref_ag.rows[i][i]
                          else:
                              sum_total = 0
                              for j in range(i + 1, num_variables):
                                  sum_total += ref_ag.rows[i][j] * solution[num_variables - 1 - j]
                              x_i = (ref_ag.rows[i][num_variables] - sum_total) / ref_ag.rows[i][i]
                          solution.append(x_i)

                      solution.reverse()
                      return Vec([round(x,10) for x in solution])




  """ ----------------- PROBLEM 5 ----------------- """


  def gram_schmidt(S: set):
      """
      returns the solution to the system Ax = b
      :param A: Matrix type; the matrix of coefficients in the system of equations
      :param b: Vec type; the vector of constants in the system of equations
      :returns:
                - None type if the system does not have a solution
                - int type; if the system has infinitely-many solutions, the number of free
                            variables is returned
                - Vec type; the vector solution of the system if it has a unique solution
      """
      # TODO: Implement this function
      result = helpers.is_independent(S)
      if not result:
          raise ValueError("The input vectors are not linearly independent.")

      # Initialize a list to store the orthogonalized vectors
      orthogonalized = []

      # Copy the input vectors into a temporary list of lists
      temp_vec_list = [v.elements[:] for v in S]

      # Perform Gram-Schmidt process
      for i in range(len(temp_vec_list)):
          for j in range(i):
              temp_vec_list[i] = projection(temp_vec_list[j], temp_vec_list[i])

      # Normalize the orthogonalized vectors and store them in orthogonalized list
      for k in range(len(temp_vec_list)):
          denominator = sum(x ** 2 for x in temp_vec_list[k]) ** 0.5
          factor = 1 / denominator if denominator != 0 else 0
          temp_vec_list[k] = [x * factor for x in temp_vec_list[k]]
          orthogonalized.append(Vec(temp_vec_list[k]))

      return orthogonalized



  """ HELPER METHOD"""


  def _pivot_idx(i: int, j: int, A: Matrix):
      """
      finds the row index >= i of the first non-zero entry
      in column j of the given Matrix.  If no non-zero entry
      exists in column j at or after row i, then None is returned.
      :param i: int type; the row index of where to begin search
      :param j: int type; the column index of where to begin search
      :param A: Matrix type; the matrix of interest
      :return: int type or None type; if int, the row index of the
               first non-zero entry in column j.
      """
      column = A.get_col(j)
      for k in range(i - 1, len(column)):
          print("column k: ",column[k])
          if column[k] != 0:
              return k + 1
      return None

  def projection(w_vector, x_vector):
      # len_vector = len(w_vector)
      numerator = sum(w * x for w, x in zip(w_vector, x_vector))
      denominator = sum(w ** 2 for w in w_vector)
      factor = numerator / denominator if denominator != 0 else 0
      temp_w_vector = [w * factor for w in w_vector]
      return [x - w for x, w in zip(x_vector, temp_w_vector)]


  if __name__ == "__main__":
      matrix1 = Matrix([[2, -1, -10], [2, 0, -4], [-7, 3, 2]])
      print("matrix: ",matrix1)
      # expected1 = Matrix([[1.0, -0.5, -5.0], [0.0, 1.0, 6.0], [-0.0, -0.0, 1.0]])
      _ref(matrix1)