""" ----------------- PROBLEM 1 ----------------- """

def primes(a, b):
  if a < 1 or b < a:
      raise ValueError("Invalid range given")

  if a == 1:
      a = 2

  stop = int(b**0.5) + 1
  P = set(range(a, b + 1))

  for x in range(2, stop + 1):
      multiples_x = set(k * x for k in range(2, (b // x) + 1))
      P -= multiples_x

  return P

""" ----------------- PROBLEM 2 ----------------- """

def bezout_coeffs(a, b):
      if a < 0 or b < 0:
          raise ValueError("bezout_coeffs(a, b) does not support negative arguments.")

      s0, t0 = 1, 0
      s1, t1 = -1 * (b // a), 1

      temp = b
      bk = a
      ak = temp % a

      while ak != 0:
          temp_s, temp_t = s1, t1

          s1 = s0 - (bk // ak) * s1
          t1 = t0 - (bk // ak) * t1

          s0, t0 = temp_s, temp_t
          temp = bk

          bk, ak = ak, temp % ak

      return {a: s0, b: t0}

""" ----------------- PROBLEM 3 ----------------- """

def gcd(a, b):
  A = abs(a)
  B = abs(b)
  if A == B:
    return A
  while B != 0:
    A, B = B, A % B
  return A

""" ----------------- PROBLEM 4 ----------------- """

def mod_inv(a, m):
    if m < 0:
        raise ValueError(f"mod_inv(a, m) does not support negative modulo m = {m}")

    g = gcd(a, m)

    if g != 1:
        raise ValueError(
            f"mod_inv(a, m) does not support integers that are not relatively prime.\nGCD of {a} and {m} is {g}."
        )

    A = a % m

    def extended_gcd(aa, bb):
        lastremainder, remainder = abs(aa), abs(bb)
        x, lastx, y, lasty = 0, 1, 1, 0

        while remainder:
            lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
            x, lastx = lastx - quotient * x, x
            y, lasty = lasty - quotient * y, y

        return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

    _, inv, _ = extended_gcd(a, m)
    inverse = inv % m

    return inverse


""" ----------------- PROBLEM 5 ----------------- """


def solve_mod_equiv(a, b, m, low, high):
  if high < low:
    raise ValueError(
      f"solve_mod_equiv() does not support the upper bound {high} less than the lower bound {low}"
    )
  if m < 0:
    raise ValueError(
      f"solve_mod_equiv() does not support negative modulo m = {m}")
  a_inv = mod_inv(a, m)
  k_low = (low - b * a_inv + m - 1) // m
  k_high = (high - b * a_inv) // m
  x = [m * k + b * a_inv for k in range(k_low, k_high + 1)]
  return set(x)
