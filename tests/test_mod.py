import unittest

from mod_bot import warnings


class TestModBot(unittest.TestCase):

    def test_warning_storage(self):

        user_id = 123

        warnings[user_id] = 1

        self.assertEqual(
            warnings[user_id],
            1
        )

    def test_warning_increment(self):

        user_id = 456

        warnings[user_id] = 0

        warnings[user_id] += 1

        self.assertEqual(
            warnings[user_id],
            1
        )


if __name__ == "__main__":

    unittest.main()
