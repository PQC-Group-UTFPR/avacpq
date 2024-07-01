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
        Initializes the GGH encryption system with the specified dimensionality.

        Args:
            n (int): The number of dimensions for the lattice vectors.
        """
        self.n = n
        self.rand = 20

    def generate_keys(self):
        """
        Generates the lattice basis B' and computes the public key U.

        Returns:
            tuple: A tuple containing the desired lattice basis B' (numpy.ndarray)
                   and the public key U (numpy.ndarray).
        """
        # Choose r automatically within a reasonable range
        r = secrets.randbelow(self.rand) + 1

        # Given lattice basis
        B = np.array(
            [
                [secrets.randbelow(r * 2 + 1) - r for _ in range(self.n)]
                for _ in range(self.n)
            ]
        )
        while np.linalg.matrix_rank(B) != self.n:
            B = np.array(
                [
                    [secrets.randbelow(r * 2 + 1) - r for _ in range(self.n)]
                    for _ in range(self.n)
                ]
            )

        # Desired lattice basis
        B_prime = np.array(
            [
                [secrets.randbelow(r * 2 + 1) - r for _ in range(self.n)]
                for _ in range(self.n)
            ]
        )
        while np.linalg.matrix_rank(B_prime) != self.n:
            B_prime = np.array(
                [
                    [secrets.randbelow(r * 2 + 1) - r for _ in range(self.n)]
                    for _ in range(self.n)
                ]
            )

        # Compute the public key U
        U = np.dot(B_prime, inv(B))

        return B_prime, U

    def generate_error(self, e):
        """
        Generate an error vector with values from -e to e (inclusive).

        Args:
            e (int): The range of values for the error vector.

        Returns:
            np.array: The generated error vector.
        """
        error = np.array([secrets.randbelow(2 * e + 1) - e for _ in range(self.n)])

        return error

    def encrypt(self, public_key, plaintext, error):
        """
        Encrypt the plaintext by multiplying it with the public key and adding error.

        Args:
            public_key (np.array): The public key used for encryption.
            plaintext (np.array): The plaintext message to be encrypted.
            error (np.array): The error vector to add to the encrypted message.

        Returns:
            np.array: The ciphertext resulting from the encryption process.
        """
        ciphertext = np.dot(plaintext, public_key) + error

        return ciphertext

    def decrypt(self, public_key_inverse, ciphertext):
        """
        Decrypt the ciphertext using the public key inverse.

        Args:
            public_key_inverse (np.array): The inverse of the public key used for decryption.
            ciphertext (np.array): The encrypted message to be decrypted.

        Returns:
            np.array: The decrypted plaintext (before Babai rounding).
        """
        decrypted_plaintext = np.dot(ciphertext, public_key_inverse)

        return decrypted_plaintext

    def babai_rounding(self, decrypted_plaintext, error, inverse_basis):
        """
        Apply Babai rounding to remove the error term if it's small enough.

        Args:
            decrypted_plaintext (np.array): The decrypted plaintext.
            error (np.array): The error vector.
            inverse_basis (np.array): The inverse of the lattice basis used for rounding.

        Returns:
            np.array: The rounded decrypted plaintext.
        """
        rounded_decrypted_plaintext = decrypted_plaintext - np.dot(error, inverse_basis)

        return rounded_decrypted_plaintext

    def recover_plaintext(self, rounded_decrypted_plaintext, public_key):
        """
        Recover the plaintext message by multiplying rounded decrypted plaintext
        with U-inverse.

        Args:
            rounded_decrypted_plaintext (np.array): The rounded decrypted plaintext.
            public_key (np.array): The public key used for encryption.

        Returns:
            np.array: The recovered plaintext message.
        """
        plaintext = np.dot(rounded_decrypted_plaintext, inv(public_key))
        plaintext = np.dot(plaintext, public_key)
        plaintext = np.round(plaintext).astype(int)

        return plaintext


# Example usage:
if __name__ == "__main__":
    # Initialize GGH with dimension n
    ggh = GGH(n=2)

    # Given plaintext
    plaintext = np.array([3, -7])

    # Generate public key
    B_prime, U = ggh.generate_keys()

    # Generate error vector
    error = ggh.generate_error(e=1)

    # Encrypt plaintext
    ciphertext = ggh.encrypt(U, plaintext, error)

    # Decrypt ciphertext
    public_key_inverse = inv(U)
    decrypted_plaintext = ggh.decrypt(public_key_inverse, ciphertext)
    rounded_decrypted_plaintext = ggh.babai_rounding(decrypted_plaintext, error, inv(U))
    recovered_plaintext = ggh.recover_plaintext(rounded_decrypted_plaintext, U)
