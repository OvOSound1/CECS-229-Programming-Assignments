import numpy as np
import structures
from copy import deepcopy
from random import randint

def initialize_matrices(m, n):
  rowsp = [[randint(-10, 10) for j in range(n)] for i in range(m)]
  matrix = structures.Matrix(rowsp)
  return [np.matrix(deepcopy(rowsp)), matrix]

def is_independent(S):
  rows = [vec.elements for vec in S]
  return np.linalg.matrix_rank(rows) == len(S)

def create_vectors(n, independent = True):
  if not independent:
    k = randint(1, n-1) # number of independent
    vecs = [structures.Vec([randint(-10, 10) for j in range(n)]) for i in range(k)]
    for r in range(n-k):
      idx = randint(0, len(vecs)-1)
      scalar = randint(2, 5)
      vecs.insert(idx, scalar* vecs[randint(0, len(vecs)-1)])
    return vecs
  else:
    vecs = [structures.Vec([randint(-10, 10) for j in range(n)]) for i in range(n)]
    while not is_independent(vecs):
       vecs = [structures.Vec([randint(-10, 10) for j in range(n)]) for i in range(n)]
    return vecs