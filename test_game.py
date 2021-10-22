import unittest

from game import Game


class GameTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.game = Game()

    def test_gutter_game(self):
        self.game.roll_many(20, 0)
        self.assertEqual(0, self.game.score())

    def test_all_one_game(self):
        self.game.roll_many(20, 1)
        self.assertEqual(20, self.game.score())

    def test_one_valueless_spare(self):
        self.game.roll_many(2, 5)  # spare
        self.game.roll_many(18, 0)
        self.assertEquals(10, self.game.score())

    def test_one_spare(self):
        self.game.roll_many(2, 5)  # spare
        self.game.roll(3)
        self.game.roll_many(17, 0)
        self.assertEquals(16, self.game.score())

    def test_one_valueless_strike(self):
        self.game.roll(10)  # strike
        self.game.roll_many(18, 0)
        self.assertEquals(10, self.game.score())

    def test_one_strike(self):
        self.game.roll(10)  # strike
        self.game.roll_many(2, 3)
        self.game.roll_many(16, 0)
        self.assertEquals(22, self.game.score())

    def test_double_strike(self):
        self.game.roll_many(2, 10)  # double strike
        self.game.roll_many(16, 0)
        self.assertEquals(40, self.game.score())

    def test_tripple_strike(self):
        self.game.roll_many(3, 10)  # tripple strike
        self.game.roll_many(14, 0)
        self.assertEquals(70, self.game.score())

    def test_ten_strikes(self):
        self.game.roll_many(10, 10)
        self.game.roll(0)
        self.assertEquals(280, self.game.score())

    def test_eleven_strikes(self):
        self.game.roll_many(11, 10)
        self.game.roll(0)
        self.assertEquals(290, self.game.score())

    def test_all_strikes(self):
        self.game.roll_many(12, 10)
        self.assertEquals(300, self.game.score())


if __name__ == '__main__':
    unittest.main()
