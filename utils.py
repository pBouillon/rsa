import math
import secrets
from typing import Tuple

import sympy


# MIT License

# Copyright (c) 2018 Pierre Bouillon

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""byte length for p and q generation
"""
BYTE_LEN = 32


def decrypt(keypair: Tuple[int, int], to_decrypt: list) -> str:
    """decrypt a message with the public key

    :param keypair: public key
    :param to_decrypt: ciphertext
    :return: the decripted message
    """
    pk, n = keypair
    # decrypting with: m = c^pk % n
    return ''.join([chr(pow(c, pk, n)) for c in to_decrypt])


def encrypt(keypair: Tuple[int, int], to_encrypt: str) -> list:
    """Encrypting the message with private key

    :param keypair: private key
    :param to_encrypt: message to encrypt
    :return: the encrypted message as a list of numbers
    """
    pk, n = keypair

    # encrypting with nb = c^pk % n
    return [pow(ord(c), pk, n) for c in to_encrypt]


def gen_keys(_p: int, _q: int) -> tuple:
    """Generating private and public keys

    :param _p: first prime number
    :param _q: second prime number
    :return: the public and private key pairs
    """
    # modulus for public and private keys
    n = _p * _q

    # totient
    # see https://simple.wikipedia.org/wiki/Euler's_totient_function
    phi = (_p - 1) * (_q - 1)

    # picking e > 1 corpime to phi
    # see https://simple.wikipedia.org/wiki/Coprime
    e = secrets.randbelow(phi) + 1
    while math.gcd(e, phi) != 1:
        e = secrets.randbelow(phi) + 1

    # evaluate d using Extended Euclidean algorithm
    # see: https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    d = sympy.mod_inverse(e, phi)

    # (e, n) -> public key pair
    # (d, n) -> private key pair
    return (e, n), (d, n)


def get_rdm_prime_nb(to_ignore=None) -> int:
    """Generate prime numbers

    :param to_ignore: blacklisted numbers
    :return: the generated prime number
    """
    if to_ignore is None:
        to_ignore = []
    found = False

    nb = 0
    while not found:
        nb = secrets.randbits(BYTE_LEN)

        # the number shouldn't be in the ignored list
        if nb in to_ignore or not is_prime(nb):
            continue

        found = True

    return nb


def is_prime(nb: int) -> bool:
    """Check if a number is a prime number or not

    :param nb: the number to check
    :return: True if prime, False otherwise
    """
    # even numbers are not prime
    if nb % 2 == 0 and nb > 2:
        return False

    # checking all numbers up to the square root of the number
    # full explanation:
    # https://stackoverflow.com/questions/18833759/python-prime-number-checker/18833870#18833870
    return all(nb % i for i in range(3, int(nb ** .5) + 1, 2))


def power(x: int, n: int) -> int:
    """Evaluate the power of big numbers numbers
    see https://en.wikipedia.org/wiki/Exponentiation_by_squaring

    :param x: number
    :param n: power
    :return: the total of x ** n
    """
    if n < 0:
        x = 1 / x
        n *= -1

    if n == 0:
        return 1

    y = 1
    while n > 1:
        if n % 2 == 0:
            x *= x
            n /= 2
        else:
            y *= x
            x *= x
            n = (n - 1) * 2

    return x * y
