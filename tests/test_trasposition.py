import src.ciphers.transposition as cipher  # The code to test
import unittest  # The test framework


class Test_Transposition(unittest.TestCase):
    def setUp(self) -> None:
        self.cipher = cipher.Columnar()
        self.cipher.key = "hello"

    def test_symmetry(self):
        message = "Hello World!"
        encoded = self.cipher.encode(message)
        decoded = self.cipher.decode(encoded)
        self.assertEqual(self.cipher._sanatise(message), decoded)


if __name__ == "__main__":
    unittest.main()
