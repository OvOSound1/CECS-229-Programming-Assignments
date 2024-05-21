import pa6
import numpy as np
from random import randint
from structures import Matrix, Vec
from helpers import initialize_matrices, create_vectors

if __name__ == "__main__":
    print("Welcome to the PA #6 Tester")

    while True:

        user_in = input(
            "\n" + "-" * 50 +
            "\nWhat would you like to test?\n1.  norm(Vec, p) \n2.  _ref(Matrix)\n3.  rank(Matrix)\n4.  gauss_solve(Matrix, Vec)\n5.  gram_schmidt(S)\nQ.  Quit\n\nEnter your selection: "
        )
        if user_in == '1':
            n = randint(3, 5)
            v = [randint(-10, 10) for i in range(n)]
            for p in [1, 2, 3, 10]:
                print('-' * 20)
                print(f"\nTesting norm({v}, {p})...")
                returned = pa6.norm(Vec(v), p)
                expected = np.linalg.norm(np.array(v), ord=p)
                print("\tReturned:", returned)
                print("\tExpected:", expected)
                if returned == expected:
                    print("\tTest passed!")
                else:
                    print(f"\tTest failed!")
        elif user_in == '2':

            matrix1 = Matrix([[2, -1, -10], [2, 0, -4], [-7, 3, 2]])
            matrix2 = Matrix([[-10, 7, 7, -3, 2], [6, -9, 7, -5, 0], [-2, 7, -3, -6, 2]])
            matrix3 = Matrix([[-7, -9, 4, -9], [2, -9, -3, 3]])
            matrices = [matrix1, matrix2, matrix3]

            expected1 = Matrix([[1.0, -0.5, -5.0], [0.0, 1.0, 6.0], [-0.0, -0.0, 1.0]])
            expected2 = Matrix([[1.0, -0.7, -0.7, 0.3, -0.2], [-0.0, 1.0, -2.333333333333333, 1.4166666666666665, -0.25],
                                [0.0, 0.0, 1.0, -1.5384615384615388, 0.34615384615384626]])
            expected3 = Matrix([[1.0, 1.2857142857142858, -0.5714285714285714, 1.2857142857142858],
                                [-0.0, 1.0, 0.16049382716049385, -0.03703703703703702]])
            refs = [expected1, expected2, expected3]
            for matrix, expected in zip(matrices, refs):
                print('-' * 20)
                m, n = matrix.dim()
                print(f"\nTesting _ref(A) for  {m}x{n} matrix A:")
                print(matrix)
                returned = pa6._ref(matrix)
                print("\nReturned:\n", returned)
                print("\nExpected:\n", expected)



        elif user_in == '3':

            k = randint(3, 5)
            dimensions = [(k, k), (randint(3, 4), randint(5, 6)), (randint(5, 6), randint(3, 4))]
            for (m, n) in dimensions:
                np_matrix, matrix = initialize_matrices(m, n)
                print('-' * 20)
                print(f"\nTesting rank(A) for {m}x{n} matrix A:")
                print(matrix)
                returned = pa6.rank(matrix)
                expected = np.linalg.matrix_rank(np_matrix)
                print("Returned:", returned)
                print("Expected:", expected)
                if returned == expected:
                    print("Test Passed!")
                else:
                    print("Test Failed!")

        elif user_in == '4':
            #  TEST 1: Unique solution
            n = randint(3, 5)
            b = [randint(-10, 10) for i in range(n)]
            A, matrix = initialize_matrices(n, n)
            while np.linalg.matrix_rank(A) != n:
                A, matrix = initialize_matrices(n, n)
            expected = Vec(list(np.linalg.solve(A, b)))

            print('-' * 20)
            print("\nTesting gauss_solve(A, b) for system with UNIQUE SOLUTION:")
            print("A:\n", matrix)
            print("\nb:", b)
            returned = pa6.gauss_solve(matrix, Vec(b))

            print(f"\nReturned:\n{returned}")
            print(f"\nExpected:\n{expected}")
            error_vec = expected - returned

            if type(returned) != type(expected):
                print(f"Expected 'Vec' type but received {type(returned)} type.")
                print("\nTest Failed!")
            elif pa6.norm(error_vec, 2) < 1e-4:
                print("\nTest Passed!")
            else:
                print("\nTest Failed!")

            #  TEST 2: Infinitely-many solutions
            m = randint(3, 5)
            d = randint(1, n-2) # number of free variables
            n = m + d
            A, matrix = initialize_matrices(m, n)
            x = Vec([randint(-10, 10) for i in range(n)])
            b = matrix * x

            print('-' * 20)
            print("\nTesting gauss_solve(A, b) for system with INFINITELY-MANY SOLUTIONS")
            print("A:\n", matrix)
            print("b:", b)
            returned = pa6.gauss_solve(matrix, b)
            expected = d
            print("\nReturned: ", returned)
            print("Expected: ", expected)
            if type(returned) != type(expected):
                print("\nTest Failed!")
            elif expected == returned:
                print("\nTest Passed!")
            else:
                print("\nTest Failed!")


            #  TEST 3: No solution
            n = randint(3, 5)
            A = [[randint(-10, 10) for j in range(n)] for i in range(n-1)]
            b = [randint(1, 10) for i in range(n-1)]
            idx = randint(0, len(A)-1)
            some_row = A[idx]
            A.append(some_row)
            b.append(b[idx] * 10000 + 100)
            matrix = Matrix(A)
            print('-' * 20)
            print("\nTesting gauss_solve(A, b) for system with NO SOLUTION")
            print("A:\n", matrix)
            print("\nb:", b)
            returned = pa6.gauss_solve(matrix, Vec(b))
            expected = None
            print("\nReturned:", returned)
            print("Expected:", expected)
            if type(returned) != type(expected):
                print("\nTest Failed!")
            elif expected == returned:
                print("\nTest Passed!")
            else:
                print("\nTest Failed!")

        elif user_in == '5':

            S = create_vectors(randint(3, 5))
            A = np.array([v.elements for v in S]).T
            print('-' * 20)
            print(f"\nTesting gram_schmidt(S) for S:")
            for v in S:
                print(str(v))
            Q, R = np.linalg.qr(A)
            returned = list(pa6.gram_schmidt(S))

            print("\nReturned:\n")
            for v in returned:
                print(v)

            expected = Q.T
            print("\nExpected:\n")
            for col in expected:
                print(col)

            if len(returned) != len(expected):
                print("Test Failed!")
            else:
                print(
                    "\nNOTE:\n(1)  Vectors may appear in different order to expected answer.\n(2)  Negatives may appear at element indices opposite to where they appear in the expected answer. This is still correct.")

        elif user_in.upper() == 'Q':
            break
        else:
            print("Invalid selection.  Please try again.\n")
