import csv
import unittest

from parameterized import parameterized

from game import Game
from game import transform_symbols


def load_game_data():
    with open("./bowling_data_5000.csv") as data_file:
        data = [line for line in csv.reader(data_file)]

    data.pop(0)  # drop first line in csv file
    return data


def custom_name_func(testcase_func, _param_num, param):
    return "%s for ['%s' -> %s]" % (
        testcase_func.__name__,
        parameterized.to_safe_name(param.args[0]),
        parameterized.to_safe_name(param.args[1])
        )


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
        self.assertEquals(30, self.game.score())

    def test_tripple_strike(self):
        self.game.roll_many(3, 10)  # tripple strike
        self.game.roll_many(14, 0)
        self.assertEquals(60, self.game.score())

    def test_ten_strikes(self):
        self.game.roll_many(10, 10)
        self.game.roll_many(2, 0)
        self.assertEquals(270, self.game.score())

    def test_eleven_strikes(self):
        self.game.roll_many(11, 10)
        self.game.roll(0)
        self.assertEquals(290, self.game.score())

    def test_all_strikes(self):
        self.game.roll_many(12, 10)
        self.assertEquals(300, self.game.score())

    def test_roll_list(self):
        self.game.roll_list([5 for _ in range(21)])
        self.assertEquals(150, self.game.score())

    def test_specific_game_data(self):
        self.game.roll_list(transform_symbols("6/XX2/2/2/4/51XXX"))
        self.assertEquals(171, self.game.score())

    # "manual" parameterized tests
    # def test_game_data(self):
    #     game_data = load_game_data()
    #     for data in game_data:
    #         self.game = Game(data[0])
    #         self.game.roll_list(transform_symbols(data[0]))
    #         self.assertEquals(int(data[1]), self.game.score())

    @parameterized.expand(load_game_data, testcase_func_name=custom_name_func)
    def test_game_data(self, sequence, score):
        self.game.roll_list(transform_symbols(sequence))
        self.assertEquals(int(score), self.game.score())


if __name__ == '__main__':
    unittest.main()
