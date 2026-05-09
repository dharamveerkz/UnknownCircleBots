import unittest

from games_bot import get_rps_result


class TestGamesBot(unittest.TestCase):

    def test_rps_draw(self):

        result = get_rps_result(
            "rock",
            "rock"
        )

        self.assertEqual(
            result,
            "Draw"
        )

    def test_rps_win(self):

        result = get_rps_result(
            "rock",
            "scissors"
        )

        self.assertEqual(
            result,
            "You Win 🎉"
        )

    def test_rps_lose(self):

        result = get_rps_result(
            "rock",
            "paper"
        )

        self.assertEqual(
            result,
            "Bot Wins 🤖"
        )


if __name__ == "__main__":

    unittest.main()
