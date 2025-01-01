import unittest
from src.queens.QueensGame import QueensGame


class QueensTestCase(unittest.TestCase):

    # @staticmethod
    # def test_produce_a_solution():
    #     game = QueensGame(8)
    #     solution=game.produce_a_solution()
    #     print(solution)

    @staticmethod
    def test_init_a_solution():
        game = QueensGame(8)
        solution = game.init_a_solution()
        print(solution)



    def test_get_queens_positions_2d(self):
        game = QueensGame(4)
        solution = [1, 3, 0, 2]
        expected = [[0, 1], [1, 3], [2, 0], [3, 2]]
        actual = game.get_queens_positions_2d(solution)
        self.assertEqual(expected, actual)

    def test_is_diagonally_touched_0(self):
        # no diagonally touched
        solution = [1, 3, 0, 2]
        game = QueensGame(4)
        flag = game.is_diagonally_touched(solution)
        self.assertEqual(False, flag)

    def test_is_diagonally_touched_1(self):
        # no diagonally touched
        solution = [2, 6, 1, 7, 5, 3, 0, 4]
        game = QueensGame(8)
        flag = game.is_diagonally_touched(solution)
        self.assertEqual(False, flag)

    def test_is_diagonally_touched_1(self):
        # (0,0) and (1,1) are diagonally touched
        solution = [0, 1, 3, 2]
        game = QueensGame(4)
        flag = game.is_diagonally_touched(solution)
        self.assertEqual(True, flag)

    @staticmethod
    def test_get_direction():
        low_chance_choices = {2}
        game = QueensGame(4)
        game.get_direction(low_chance_choices, 3)

    @staticmethod
    def test_set_color_around():
        board_color_region = [[-1, -1, 1, -1, -1, 0, 0, -1],
                              [-1, -1, 1, -1, -1, 0, -1, -1],
                              [-1, -1, -1, -1, 2, 0, 0, -1],
                              [-1, 3, -1, -1, 2, 2, 2, 2],
                              [-1, 3, -1, -1, 4, 4, -1, -1],
                              [-1, -1, -1, 6, 4, 4, 4, 5],
                              [-1, -1, -1, 6, -1, 4, 4, 5],
                              [7, -1, -1, -1, -1, 4, -1, -1]]

        game = QueensGame(8)
        board_color_region = game.set_color_around(board_color_region)
        print(board_color_region)

    @staticmethod
    def test_set_color():
        game = QueensGame(8)
        queens_positions = [6, 2, 4, 1, 5, 7, 3, 0]
        board_color_region = game.get_board_color_region(queens_positions)
        print(board_color_region)