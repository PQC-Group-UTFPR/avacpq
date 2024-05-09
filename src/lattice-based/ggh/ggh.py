import numpy as np
from numpy.linalg import inv
import secrets


class GGH:
    """
    Goldreich-Goldwasser-Halevi (GGH) encryption system implementation.

    The GGH class provides functionalities for generating keys, encrypting and
    decrypting messages using the GGH encryption system. It operates on vectors
    in a lattice-based cryptosystem.
    """

    def __init__(self, n):
        """
        Initializes the GGH encryption system with the specified dimensionality
        """
        self.n = n

    def generate_random_matrix(self, r):
        """
        Generates a random matrix of size (n x n) with elements in the range [0, r).
        """
        matrix = np.array(
            [[secrets.randbelow(r) for _ in range(self.n)] for _ in range(self.n)]
        )
        while np.linalg.matrix_rank(matrix) != self.n:
            matrix = np.array(
                [[secrets.randbelow(r) for _ in range(self.n)] for _ in range(self.n)]
            )
        return matrix

    def generate_keys(self, r):
        """
        Generates the lattice basis B' and computes the public key U
        """
        # Given lattice basis
        B = self.generate_random_matrix(r)

        # Desired lattice basis
        B_prime = self.generate_random_matrix(r)

        # Compute the public key U
        U = np.dot(B_prime, inv(B))
        return B_prime, U

    def encrypt(self, public_key, plaintext, error):
        """
        Encrypt the plaintext by multiplying it with the public key and adding
        error
        """
        ciphertext = np.dot(plaintext, public_key) + error
        return ciphertext

    def decrypt(self, public_key_inverse, ciphertext):
        """
        Decrypt the ciphertext using the public key inverse
        """
        decrypted_plaintext = np.dot(ciphertext, public_key_inverse)
        return decrypted_plaintext

    def babai_rounding(self, decrypted_plaintext, error, inverse_basis):
        """
        Babai rounding to remove the error term if it's small enough
        """
        rounded_decrypted_plaintext = decrypted_plaintext - np.dot(error, inverse_basis)
        return rounded_decrypted_plaintext

    def recover_plaintext(self, rounded_decrypted_plaintext, public_key):
        """
        Recover plaintext message by multiplying rounded decrypted plaintext
        with U-inverse
        """
        plaintext = np.dot(rounded_decrypted_plaintext, inv(public_key))
        plaintext = np.dot(plaintext, public_key)
        plaintext = np.round(plaintext).astype(int)
        return plaintext


# Example usage:
if __name__ == "__main__":
    # Initialize GGH with dimension n
    ggh = GGH(n=2)

    # Generate public key
    B_prime, U = ggh.generate_keys(r=11)
    print("Public Key:")
    for i in range(ggh.n):
        B_prime_row = B_prime[i]
        U_row = U[:, i]
        result_row = np.dot(U_row, B_prime)
        print("  ", result_row)

    # Given error vector
    error = np.array([1, -1])

    # Given plaintext
    plaintext = np.array([3, -7])

    # Encrypt plaintext
    ciphertext = ggh.encrypt(U, plaintext, error)
    print("Plaintext:", plaintext)
    print("Ciphertext:", ciphertext)

    # Decrypt ciphertext
    public_key_inverse = inv(U)
    decrypted_plaintext = ggh.decrypt(public_key_inverse, ciphertext)
    rounded_decrypted_plaintext = ggh.babai_rounding(decrypted_plaintext, error, inv(U))
    recovered_plaintext = ggh.recover_plaintext(rounded_decrypted_plaintext, U)
    print("Recovered plaintext:", recovered_plaintext)
