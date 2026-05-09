import unittest

from ai_bot import user_last_ask


class TestAIBot(unittest.TestCase):

    def test_rate_limit_storage(self):

        user_id = 100

        user_last_ask[user_id] = 999

        self.assertEqual(
            user_last_ask[user_id],
            999
        )

    def test_user_exists(self):

        user_id = 200

        user_last_ask[user_id] = 123

        self.assertTrue(
            user_id in user_last_ask
        )


if __name__ == "__main__":

    unittest.main()
