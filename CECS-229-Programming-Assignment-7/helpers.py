import copy
from structures import Matrix, Vec

def norm(v: Vec, p: int):
    return sum(abs(v.elements[i])**p for i in range(len(v.elements)))**(1 / p)

def is_independent(S):
    rows = [vec.elements for vec in S]
    A = Matrix(rows)
    return rank(A) == len(S)

def gram_schmidt(S):
    if not is_independent(S):
        raise ValueError("The vectors are not linearly independent")

    ortho_basis = []
    for v in S:
        w = Vec(v.elements)
        for u in ortho_basis:
            proj = (v * u / (u * u)) * u
            w = w - proj
        if abs(w) > 1E-10:
            ortho_basis.append(w / norm(w, 2))
    return ortho_basis

def _ref(A: Matrix):
    A = copy.deepcopy(A)
    m, n = A.dim()
    for i in range(min(m, n)):
        pivot_idx = _pivot_idx(i + 1, i + 1, A)
        if pivot_idx is not None:
            A.rows[i], A.rows[pivot_idx - 1] = A.rows[pivot_idx - 1], A.rows[i]
            pivot = A.get_entry(i + 1, i + 1)
            if abs(pivot) < 1E-10:
                continue  # Skip near-zero pivot
            for k in range(i, n):
                A.set_entry(i + 1, k + 1, A.get_entry(i + 1, k + 1) / pivot)
            for j in range(i + 1, m):
                factor = A.get_entry(j + 1, i + 1)
                for k in range(i, n):
                    A.set_entry(j + 1, k + 1, A.get_entry(j + 1, k + 1) - factor * A.get_entry(i + 1, k + 1))
    return A

def rank(A: Matrix):
    ref_A = _ref(A)
    rank = 0
    m, n = ref_A.dim()
    for i in range(m):
        if any(abs(ref_A.get_entry(i + 1, j + 1)) > 1E-6 for j in range(n)):
            rank += 1
    return rank

def frobenius_norm(A: Matrix):
    f = 0
    m, n = A.dim()
    for i in range(m):
        for j in range(n):
            f += abs(A.get_entry(i + 1, j + 1))**2
    return f**0.5

count = {
    1: 'First',
    2: 'Second',
    3: 'Third',
    4: 'Fourth',
    5: 'Fifth',
    6: 'Sixth',
    7: 'Seventh',
    8: 'Eighth',
    9: 'Ninth',
    10: 'Tenth'
}

def _pivot_idx(i: int, j: int, A: Matrix):
    column = A.get_col(j)
    for k in range(i - 1, len(column)):
        if abs(column[k]) > 1E-6:
            return k + 1
        else:
            A.set_entry(k + 1, j, 0)
    return None