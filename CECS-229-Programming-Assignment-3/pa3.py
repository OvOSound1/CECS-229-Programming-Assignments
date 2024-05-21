""" ----------------- PROBLEM 1 ----------------- """

import math

def affine_encrypt(text, a, b):

  if math.gcd(a, 26) != 1:
    raise ValueError("a and 26 are not coprime")

  cipher = ""
  for letter in text:
    if letter.isalpha():

      num = ord(letter.upper()) - ord('A')

      cipher_num = (a * num + b) % 26

      cipher += chr(cipher_num + ord('A'))

  return cipher

""" ----------------- PROBLEM 2 ----------------- """

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def modular_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("The modular inverse does not exist.")
    else:
        return x % m

def affine_decrypt(ciphertext, a, b):
    if math.gcd(a, 26) != 1:
        raise ValueError("The given key is invalid.")

    a_inv = modular_inverse(a, 26)

    text = ""
    for letter in ciphertext:
        if letter.isalpha():
            letter = letter.upper()

            num = ord(letter) - 65

            decrypted_num = (a_inv * (num - b)) % 26

            decrypted_letter = chr(decrypted_num + 65)

            text += decrypted_letter

    return text


""" ----------------- PROBLEM 3 ----------------- """

def encryptRSA(plaintext, n, e):

  text = plaintext.replace(' ', '')

  digits = ''.join(str(ord(c) - 65).zfill(2) for c in text.upper())

  l = len(str(n))

  while len(digits) % l != 0:
      digits += '23'

  blocks = [digits[i:i + l] for i in range(0, len(digits), l)]
  cipher = ""
  for b in blocks:

      encrypted_block = str(pow(int(b), e, n)).zfill(l)

      cipher += encrypted_block

  return cipher

""" ----------------- PROBLEM 4 ----------------- """
def decryptRSA(cipher, p, q, e):

  n = p * q
  ciphertext = cipher.replace(' ', '')

  l = len(str(n))

  blocks = [ciphertext[i:i + l] for i in range(0, len(ciphertext), l)]

  text = ""

  phi = (p - 1) * (q - 1)

  def extended_gcd(a, b):
      if a == 0:
          return b, 0, 1
      else:
          g, x, y = extended_gcd(b % a, a)
          return g, y - (b // a) * x, x

  g, x, _ = extended_gcd(e, phi)
  if g != 1:
      raise Exception('Modular inverse does not exist')
  else:
      e_inv = x % phi

  for b in blocks:
      decrypted_block = str(pow(int(b), e_inv, n)).zfill(l)

      while len(decrypted_block) < l:
          decrypted_block = '0' + decrypted_block

      text += ''.join(chr(int(decrypted_block[i:i + 2]) + 65) for i in range(0, len(decrypted_block), 2))

  return text
