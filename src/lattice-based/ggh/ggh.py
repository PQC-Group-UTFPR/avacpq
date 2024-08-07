import numpy as np
from numpy.linalg import inv
import secrets
from datetime import datetime

# Print debug messages?
debug = True


def debug_print(message, variable=None):
    """
    Prints debug messages with a timestamp if debug mode is enabled.

    Args:
        message (str): The debug message to print.
        variable (optional): Additional variable to print alongside the message.
    """
    if debug:
        current_time = datetime.now().strftime("%H:%M")
        print(f"[DEBUG-{current_time}] {message}")
        if variable is not None:
            print(variable)


def get_user_choice():
    """
    Prompts the user to choose between using a hardcoded plaintext or a random one.

    Returns:
        bool: True if the user chooses random plaintext, False otherwise.
    """
    choice = (
        input("Do you want to use the hardcoded plaintext or a random one? (h/r): ")
        .strip()
        .lower()
    )
    return choice == "r"


def get_dimensions():
    """
    Prompts the user to enter the number of dimensions for the plaintext vector.

    Returns:
        int: The number of dimensions.
    """
    return int(input("Enter the number of dimensions: ").strip())


def generate_random_plaintext(n, r):
    """
    Generates a random plaintext vector of specified dimensions and range.

    Args:
        n (int): The number of dimensions for the plaintext vector.
        r (int): The range for the random values in the plaintext vector.

    Returns:
        numpy.ndarray: The generated random plaintext vector.
    """
    plaintext = np.array([secrets.randbelow(r) - (r / 2) for _ in range(n)])
    return plaintext


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
        debug_print(f"Chosen r: {r}")

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
        debug_print("Lattice basis B:", B)

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
        debug_print("Desired lattice basis B_prime:", B_prime)

        # Compute the public key U
        U = np.dot(B_prime, inv(B))
        debug_print("Public key U:", U)

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
        debug_print("Error vector:", error)

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
        debug_print("Ciphertext:", ciphertext)

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
        debug_print("Decrypted plaintext (before Babai rounding):", decrypted_plaintext)

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
        debug_print("Rounded decrypted plaintext:", rounded_decrypted_plaintext)

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
    # Check if user wants random or hardcoded input
    use_random_plaintext = get_user_choice()

    # Initialize GGH with dimension n
    if use_random_plaintext:
        n = get_dimensions()
    else:
        n = 2
    ggh = GGH(n=n)

    # Given plaintext
    if use_random_plaintext:
        plaintext = generate_random_plaintext(n, ggh.rand)
    else:
        plaintext = np.array([3, -7])
    debug_print("Message plaintext", plaintext)

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
    debug_print("Recovered plaintext:", recovered_plaintext)
