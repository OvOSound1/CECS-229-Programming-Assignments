from structures import Vec, Matrix
from helpers import gram_schmidt
import numpy as np
import cmath


# ----------------------- PROBLEM 1 ----------------------- #
def qr_solve(A: Matrix, b: Vec):
    try:
        U = gram_schmidt([Vec(col) for col in A.get_columns()])
    except ValueError as e:
        print(e)
        print("Using least-squares solution due to linear dependence.")
        A_np = np.array(A.get_rows())
        b_np = np.array(b.elements)
        x_np, residuals, rank, s = np.linalg.lstsq(A_np, b_np, rcond=None)
        return Vec(x_np.tolist())

    n = len(U)
    Q = Matrix([[0 for _ in range(len(A.get_rows()))] for _ in range(len(A.get_rows()))])
    R = Matrix([[0 for _ in range(len(A.get_rows()))] for _ in range(len(A.get_columns()))])

    for j in range(n):
        Q.set_col(j + 1, U[j])
        for i in range(j + 1):
            R.set_entry(i + 1, j + 1, U[i] * Vec(A.get_col(j + 1)))

    b_star = Q.transpose() * b
    x = [0 for _ in range(n)]
    for i in reversed(range(n)):
        x[i] = b_star[i]
        for j in range(i + 1, n):
            x[i] -= R.get_entry(i + 1, j + 1) * x[j]
        x[i] /= R.get_entry(i + 1, i + 1)
    return Vec(x)


# ----------------------- PROBLEM 2 ----------------------- #
def _submatrix(A: Matrix, i: int, j: int):
    m, n = A.dim()
    if i <= 0 or i > m or j <= 0 or j > n:
        raise ValueError("Invalid indices")

    submatrix_rows = [row[:j - 1] + row[j:] for row in A.get_rows()[:i - 1] + A.get_rows()[i:]]
    return Matrix(submatrix_rows)


# ----------------------- PROBLEM 3 ----------------------- #
def determinant(A: Matrix):
    m, n = A.dim()
    if m != n:
        raise ValueError(f"Determinant is not defined for {m}x{n} Matrix. Must be square.")
    if n == 1:
        return A.get_entry(1, 1)
    elif n == 2:
        return A.get_entry(1, 1) * A.get_entry(2, 2) - A.get_entry(1, 2) * A.get_entry(2, 1)
    else:
        d = 0
        for j in range(1, n + 1):
            d += ((-1) ** (1 + j)) * A.get_entry(1, j) * determinant(_submatrix(A, 1, j))
        return d


# ----------------------- PROBLEM 4 ----------------------- #
def eigen_wrapper(A: Matrix):
    anp = np.array(A.get_rows())
    eigenVal, eigenVec = np.linalg.eig(anp)
    eigen_dict = {}
    for i in range(len(eigenVal)):
        eigen_dict[eigenVal[i]] = Vec(eigenVec[:, i].tolist())
    return eigen_dict


# ----------------------- PROBLEM 5 ----------------------- #
def svd(A: Matrix):
    m, n = A.dim()
    aTa = A.transpose() * A
    eigen = eigen_wrapper(aTa)
    eigenvalues = sorted(eigen.keys(), key=abs, reverse=True)

    V = Matrix([[0 for _ in range(n)] for _ in range(n)])
    for j in range(n):
        V.set_col(j + 1, eigen[eigenvalues[j]])

    singular_values = [cmath.sqrt(value).real for value in eigenvalues]
    Sigma = Matrix([[0 for _ in range(n)] for _ in range(m)])
    for i in range(min(m, n)):
        Sigma.set_entry(i + 1, i + 1, singular_values[i])

    U = Matrix([[0 for _ in range(m)] for _ in range(m)])
    for j in range(min(m, n)):
        if singular_values[j] != 0:
            u_col = (A * V.get_col(j + 1)) * (1 / singular_values[j])
            U.set_col(j + 1, u_col)

    return U, Sigma, V