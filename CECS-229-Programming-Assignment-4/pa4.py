import math

""" ----------------- PROBLEM 1 ----------------- """
def translate(S, z0):
  """
  translates the complex numbers of set S by z0
  :param S: set type; a set of complex numbers
  :param z0: complex type; a complex number
  :return: set type; a set consisting of points in S translated by z0
  """
  translated_set = set()
  for complex_num in S:
      translated_set.add(complex_num + z0)
  return translated_set


""" ----------------- PROBLEM 2 ----------------- """
def scale(S, k):
  """
  scales the complex numbers of set S by k.  
  :param S: set type; a set of complex numbers
  :param k: float type; positive real number
  :return: set type; a set consisting of points in S scaled by k
  :raise: raises ValueError if k <= 0       
  """
  if k <= 0:
      raise ValueError("k must be a positive real number.")

  scaled_set = set()
  for complex_num in S:
      scaled_set.add(complex_num * k)
  return scaled_set


""" ----------------- PROBLEM 3 ----------------- """
def rotate(S, tau):
    """
    rotates the complex numbers of set S by tau radians.  
    :param S: set type; - set of complex numbers
    :param tau: float type; radian measure of the rotation value. 
                If negative, the rotation is clockwise.  
                If positive the rotation is counterclockwise. 
                If zero, no rotation.
    :returns: set type; a set consisting of points in S rotated by tau radians
    """
    rotated_set = set()
    for complex_num in S:
        rotated_set.add(complex_num * math.e**(1j*tau))
    return rotated_set


""" ----------------- PROBLEM 4 ----------------- """
class Vec:
  def __init__(self, contents = []):
      self.elements = list(contents)

  def __abs__(self):
      return math.sqrt(sum(e**2 for e in self.elements))

  def __add__(self, other):
      if len(self.elements) != len(other.elements):
          raise ValueError("Vectors must be the same length")
      return Vec([a + b for a, b in zip(self.elements, other.elements)])

  def __sub__(self, other):
      if len(self.elements) != len(other.elements):
          raise ValueError("Vectors must be the same length")
      return Vec([a - b for a, b in zip(self.elements, other.elements)])

  def __mul__(self, other):
      if isinstance(other, Vec):
          if len(self.elements) != len(other.elements):
              raise ValueError("Vectors must be the same length")
          return sum(a * b for a, b in zip(self.elements, other.elements))
      elif isinstance(other, (float, int)):
          return Vec([a * other for a in self.elements])

  def __rmul__(self, other):
      return self.__mul__(other)

  def __str__(self):
      return str(self.elements)