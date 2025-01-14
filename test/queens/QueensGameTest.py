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

    def test_is_diagonally_touched_2(self):
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

    # @staticmethod
    # def test_set_color_around():
    #     board_color_region = [[-1, -1, 1, -1, -1, 0, 0, -1],
    #                           [-1, -1, 1, -1, -1, 0, -1, -1],
    #                           [-1, -1, -1, -1, 2, 0, 0, -1],
    #                           [-1, 3, -1, -1, 2, 2, 2, 2],
    #                           [-1, 3, -1, -1, 4, 4, -1, -1],
    #                           [-1, -1, -1, 6, 4, 4, 4, 5],
    #                           [-1, -1, -1, 6, -1, 4, 4, 5],
    #                           [7, -1, -1, -1, -1, 4, -1, -1]]
    #     count_per_color_group = [0, 1, 2, 3, 4, 5, 6, 7]
    #     game = QueensGame(8)
    #     board_color_region = game.set_color_around(board_color_region, count_per_color_group)
    #     print(board_color_region)

    @staticmethod
    def test_set_color():
        game = QueensGame(8)
        queens_positions = [6, 2, 4, 1, 5, 7, 3, 0]
        board_color_region = game.get_board_color_region(queens_positions)
        print(board_color_region)

    def test_is_blank(self):
        game = QueensGame(8)
        queens_positions = [1, 4, 7, 5, 3, 0, 6, 2]
        flag = game.is_blank(queens_positions)
        self.assertEqual(False, flag)

    def test_is_same_col(self):
        game = QueensGame(8)
        queens_positions = [1, 4, 7, 5, 3, 0, 6, 2]
        flag = game.is_same_col(queens_positions)
        self.assertEqual(False, flag)

    def test_is_same_color(self):
        game = QueensGame(8)
        queens_positions = [1, 4, 7, 5, 3, 0, 6, 2]
        board_color_region = [[0, 0, 1, 1, 1, 1, 1, 2],
                              [1, 1, 1, 1, 1, 1, 2, 2],
                              [1, 1, 1, 4, 4, 2, 2, 2],
                              [1, 3, 1, 1, 4, 4, 4, 2],
                              [1, 3, 7, 5, 4, 4, 6, 6],
                              [3, 3, 7, 5, 5, 5, 6, 6],
                              [7, 3, 7, 5, 5, 5, 6, 6],
                              [7, 7, 7, 7, 5, 5, 6, 6]]
        flag = game.is_same_color(queens_positions, board_color_region)
        self.assertEqual(False, flag)

    def test_set_color_by_tracking_link_list(self):
        game=QueensGame(10)
        queens_positions=[8,3,0,7,4,2,6,9,5,1]
        board_color_region= [ [0,0,0,1,1,1,1,1,1,1],
                              [0,2,2,2,2,3,3,3,5,1],
                              [0,2,2,3,3,3,3,5,5,6],
                              [7,2,2,3,3,8,8,5,8,6],
                              [7,2,3,3,3,8,8,8,8,6],
                              [7,9,9,3,8,8,4,4,4,6],
                              [7,9,3,3,8,4,4,4,4,6],
                              [7,9,1,8,8,4,4,4,4,6],
                              [7,9,8,8,8,8,4,4,4,6],
                              [7,7,6,6,6,6,6,6,6,6]
                        ]

        tracking_link_list=[[(1,1),(1,2),(2,1),(2,2),(3,1),(3,2),(4,1),(4,2),(6,2),(7,2),(8,2),(9,2)], # 3 cols contains 3 colors, others are invalid
                            [(1,0),(1,5),(1,6),(1,7),(1,8),(1,9)], # 1 row contains 1 color, others are invalid
                            [(0,0),(0,1),(0,2)], # 1 row contains 1 color, others are invalid
                            [(2,0)], # queen  out of the same color
                            [(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),(2,9),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,9)], # queen's row, col and diagnoal
                            [(9,1)], # queen  out of the same color
                            [(5,1),(6,1),(7,1),(8,1),(9,3),(9,4),(9,5),(9,6),(9,7),(9,8),(9,9)], # queen's row, col and diagnoal
                            [(5,2)], # queen out of the same color
                            [(4,3),(5,3),(6,3),(5,4),(5,5),(5,6),(5,7),(5,8),(5,9)], # queen's row, col and diagnoal
                            [(3,7)],  # queen out of the same color
                            [(3,3),(3,4),(3,5),(3,6),(3,8),(3,9),(4,7),(4,8),(4,6),(0,7),(6,7),(7,7),(8,7)], # queen's row, col and diagnoal
                            [(4,4)],  # queen out of the same color
                            [(4,5),(4,9),(0,4),(1,4),(6,4),(7,4),(8,4)],  # queen's row, col and diagnoal
                            [(1,3)],  # queen out of the same color
                            [(0,3),(7,3),(8,3)],  # queen's row, col and diagnoal
                            [(8,5)],  # queen out of the same color
                            [((7,6),(8,6),(7,5),(6,5),(0,5),(8,8),(8,9))],  # queen's row, col and diagnoal
                            [(0,9)],  # 1 col contains 1 color, others are invalid
                            [(6,8),(7,8)],  # 1 color's row, col and diagnoal intersection
                            [(6,6)], # queen out of the same color
                            [(0,6),(6,9)],   # queen's row, col and diagnoal
                            [(0,8)], # queen out of the same color
                            [(7,9)] 

                        ]