import itertools
import warnings
import numpy


class Columnar:
    """Performs the Columnar transposition.

    https://en.wikipedia.org/wiki/Transposition_cipher,
    decodes and encodes using the Columnar transposition and double transposition
    also helps brute force the keys.

    Attributes:
        key : str - The ciphers key
        _collision_check : bool - Whether a collision check should be performed on encode
        _length : int - Length of the key
        _encode_order : list[int] - Order for encoding columns
        _decode_order : list[int] - Order for decoding columns
    """

    def __init__(self, key: str = "", collision_check: bool = True) -> None:
        self._length: int
        self._encode_order: list[int]
        self._decode_order: list[int]
        self.key = key
        self._collision_check = collision_check

    @property
    def key(self) -> str:
        return self._key

    @key.setter
    def key(self, key: str) -> None:
        if key == "":
            # Allows no key for bruteforcing
            self._key = ""
            self._length = 0
            self._encode_order = []
            self._decode_order = []
            return

        self._key = self._sanatise(key)

        if not self._key.isalpha():
            raise TypeError("[!!] Key must be alpha (no numbers or symbols)")

        self._length = len(self._key)
        self._encode_order = list(
            numpy.argsort(list(self._key.encode("ascii")))
        )  # Orders the positions of the letters based on ascii encoding
        self._decode_order = list(numpy.argsort(self._encode_order))

    def encode(self, message: str, applications: int = 1) -> str:
        """Encodes a plaintext message, applications times.

        Args:
            message: str - Plaintext to encode.
            applications: int - Number of times to encode

        Returns:
            Uppercase ciphertext

        Raises:
            KeyError: No key was defined
            warning: Message is non-alpha
            warning: Collision occurred
        """
        if not self._key:
            raise KeyError("[!!] Key is required to encode")

        message = self._sanatise(message)
        if not message.isalpha():
            warnings.warn(
                "[!] Message: %s is not alpha, may be easier to decode" % message
            )

        if self._collision_check:
            orig = message

        for _ in range(applications):
            message = self._sanatise(message)
            columns = [message[i :: self._length] for i in range(self._length)]
            transposed = [columns[i] for i in self._encode_order]
            message = " ".join(transposed)

        if self._collision_check:
            # Check if ciphertext == plaintext
            if self._sanatise(message) == self._sanatise(orig):
                warnings.warn("[!] Collision occurred at: %i" % applications)

        return message

    def decode(self, message: str, applications: int = 1) -> str:
        """Decodes a ciphertext, applications times.

        Args:
            message: str - Ciphertext to decode
            applications: int - Number of times to decode

        Returns:
            Uppercase plaintext with no spaces.

        Raises:
            KeyError: No key was defined
        """
        if not self._key:
            raise KeyError("[!!] Key is required to decode")

        for app in range(applications):
            transposed = self.partial_decode(message)
            columns = [transposed[i] for i in self._decode_order]
            message = ""
            max_column = max(columns, key=len)
            for i in range(len(max_column)):
                message += "".join([j[i] if len(j) > i else "" for j in columns])

            if applications > 1:  #  and app < applications - 1
                # If ciphertext is not squre the first few columns will have an additional element
                # Need to space these properly as otherwise unable to decode further
                j = 0
                for i in range(len(columns)):
                    j += len(columns[i])
                    message = message[:j] + " " + message[j:]
                    j += 1

                """                
                new = ""
                chunk_size = len(message) // self._length
                irregular_chunks = len(message) % self._length
                message = [
                    message[i : i + chunk_size]
                    for i in range(0, len(message), self._length)
                ]
                message = [
                    message[i : i + chunk_size]
                    for i in range(0, len(message), chunk_size)
                ]  # Only for squares"""

                """
                unbalanced = " ".join(
                    message[i : i + len(max_column)]
                    for i in range(
                        0, columns.count(max_column) * len(max_column), len(max_column)
                    )
                )
                balanced = " ".join(
                    message[i : i + len(max_column) - 1]
                    for i in range(
                        columns.count(max_column) * len(max_column),
                        len(message),
                        len(max_column) - 1,
                    )
                )
                
                message = unbalanced + " " + balanced
                """
                print("%i message: %s" % (app, message))

        return self._sanatise(message)

    def force_decode(self, message: str) -> str:
        """Allows the user to bruteforce the ciphertext. (Works best for passes=1)

        Args:
            message: str - Ciphertext to decode
        """
        decoded = self.partial_decode(message)
        permutations = list(
            itertools.permutations(decoded)
        )  # TODO : Might not need to make this a list
        column_length = len(max(decoded, key=len))

        for permutation in permutations:
            # Iterate through all permutations to identify the correct transposition
            for i in range(column_length):
                for j in permutation:
                    if len(j) <= i:
                        pass
                    else:
                        print("%s " % j[i], end="")
                print(" ")
            correct = input(">> Correct(Y/): ")

            if correct == "y":
                # Correct found
                self._reverse_key(decoded, permutation)
                return self.decode(message)

    def _reverse_key(self, transposed: list[str], columns: list[str]) -> None:
        """Reverse engineers the key by comparing the correct trasposition with the origional.

        Args:
            transposed: list[str] - The origional ciphertext transposition
            columns: list[str] - The correctly ordered transposition
        """
        decode_order = []
        for column in columns:
            decode_order.append(transposed.index(column))

        encode_order = list(numpy.argsort(decode_order))
        key = ""
        for i in encode_order:
            # Keys are not unique, only requires the order is the same between elements
            key += chr(97 + i)

        self._key = key
        print("Key: %s" % self._key)

    @staticmethod
    def partial_decode(message: str) -> list[str]:
        """Decode the message into columns."""
        return message.split(" ")

    @staticmethod
    def _sanatise(message: str) -> str:
        """Sanatise the message."""
        return message.replace(" ", "").upper()


if __name__ == "__main__":
    a = Columnar("hi")
    i = 56
    encoded = a.encode("Hello World!", i)
    print(encoded)
    decoded = a.decode(encoded, i)
    print(decoded)
