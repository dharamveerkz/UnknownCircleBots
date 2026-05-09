import unittest

from utils.helpers import generate_random_string


class TestFunBot(unittest.TestCase):

    def test_random_string_length(self):

        value = generate_random_string(10)

        self.assertEqual(
            len(value),
            10
        )

    def test_random_string_type(self):

        value = generate_random_string(5)

        self.assertIsInstance(
            value,
            str
        )


if __name__ == "__main__":

    unittest.main()
