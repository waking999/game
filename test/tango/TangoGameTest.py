import unittest

from src.tango.TangoGame import TangoGame

SUN = 1
MOON = 3
BLANK = 2


class TangoGameTests(unittest.TestCase):

    def test_breach_rule2_0(self):
        # no piece
        game = TangoGame(0)
        solution = [[BLANK] * game.cols for _ in range(game.rows)]
        flag = game.breach_rule2(solution)
        self.assertEqual(False, flag)

    def test_breach_rule2_1(self):
        # only 1 piece by row or col
        solution = [[BLANK, SUN, BLANK, BLANK, BLANK, BLANK],
                    [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK],
                    [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK],
                    [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK],
                    [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK],
                    [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK]
                    ]

        game = TangoGame(0)
        flag = game.breach_rule2(solution)
        self.assertEqual(False, flag)

    def test_breach_rule2_2a(self):
        # only 2 connected by row
        solution = [[BLANK, SUN, SUN, BLANK, BLANK, BLANK],
                    [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK],
                    [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK],
                    [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK],
                    [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK],
                    [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK]
                    ]

        game = TangoGame(0)
        flag = game.breach_rule2(solution)
        self.assertEqual(False, flag)

    def test_breach_rule2_2b(self):
        # only 2 connected by col
        solution = [[BLANK, SUN, BLANK, BLANK, BLANK, BLANK],
                    [BLANK, SUN, BLANK, BLANK, BLANK, BLANK],
                    [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK],
                    [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK],
                    [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK],
                    [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK]
                    ]

        game = TangoGame(0)
        flag = game.breach_rule2(solution)
        self.assertEqual(False, flag)

    def test_breach_rule2_3a(self):
        # 3 connected by row
        solution = [[BLANK, SUN, SUN, SUN, BLANK, BLANK],
                    [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK],
                    [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK],
                    [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK],
                    [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK],
                    [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK]
                    ]

        game = TangoGame(0)
        flag = game.breach_rule2(solution)
        self.assertEqual(True, flag)

    def test_breach_rule2_3b(self):
        # 3 connected by col
        solution = [[BLANK, SUN, BLANK, BLANK, BLANK, BLANK],
                    [BLANK, SUN, BLANK, BLANK, BLANK, BLANK],
                    [BLANK, SUN, BLANK, BLANK, BLANK, BLANK],
                    [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK],
                    [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK],
                    [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK]
                    ]

        game = TangoGame(0)
        flag = game.breach_rule2(solution)
        self.assertEqual(True, flag)

    def test_breach_rule3_0(self):
        # right count of each character by row and col
        solution = [[SUN, SUN, MOON, MOON, SUN, MOON],
                    [SUN, SUN, MOON, MOON, SUN, MOON],
                    [MOON, MOON, SUN, SUN, MOON, SUN],
                    [MOON, MOON, SUN, SUN, MOON, SUN],
                    [SUN, SUN, MOON, MOON, SUN, MOON],
                    [MOON, MOON, SUN, SUN, MOON, SUN],
                    ]

        game = TangoGame(0)
        flag = game.breach_rule3(solution)
        self.assertEqual(False, flag)

    def test_breach_rule3_1(self):
        # wrong count of each character by row and col
        solution = [[SUN, MOON, MOON, MOON, SUN, MOON],
                    [SUN, SUN, MOON, MOON, SUN, MOON],
                    [MOON, MOON, SUN, SUN, MOON, SUN],
                    [MOON, MOON, SUN, SUN, MOON, SUN],
                    [SUN, SUN, MOON, MOON, SUN, MOON],
                    [MOON, MOON, SUN, SUN, MOON, SUN],
                    ]

        game = TangoGame(0)
        flag = game.breach_rule3(solution)
        self.assertEqual(True, flag)

    def test_breach_rule3_2(self):
        # random solution
        solution = [[3, 1, 1, 3, 1, 3],
                    [3, 1, 1, 3, 1, 3],
                    [1, 1, 3, 3, 1, 3],
                    [3, 3, 1, 3, 1, 1],
                    [3, 1, 3, 3, 1, 1],
                    [1, 1, 3, 3, 1, 3]
                    ]

        game = TangoGame(0)
        flag = game.breach_rule3(solution)
        self.assertEqual(True, flag)

    def test_is3_connected_bypos_0(self):
        # connected
        row = [3, 2, 4, 0, 1, 5]
        game = TangoGame(0)
        flag = game.is_3connected_bypos(row)
        self.assertEqual(True, flag)

    def test_is3_connected_bypos1(self):
        # not connected
        row = [3, 2, 5, 0, 1, 4]
        game = TangoGame(0)
        flag = game.is_3connected_bypos(row)
        self.assertEqual(False, flag)

    def test_is3_connected_bvval_0(self):
        # connected
        row = [1, 1, 3, 3, 3, 1]
        game = TangoGame(0)
        flag = game.is_3connected_byval(row)
        self.assertEqual(True, flag)

    def test_is3_connected_bvval_1(self):
        # not connected
        row = [1, 1, 3, 3, 1, 3]
        game = TangoGame(0)
        flag = game.is_3connected_byval(row)
        self.assertEqual(False, flag)

    @staticmethod
    def test_produce_a_solution():
        game = TangoGame(0)
        game.produce_a_solution()

    @staticmethod
    def test_provide_clue():
        game = TangoGame(0)
        solution = game.init_a_solution()
        board = [[BLANK] * game.cols for _ in range(game.rows)]
        level=0
        board, boardClickable, signPos = game.provide_clue(solution, board,level)
        print(board)
        print(boardClickable)
        print(signPos)

    def test_is_solved_0(self):
        solution = [[1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]
                    ]

        board = [[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]
                 ]
        game = TangoGame()
        flag = game.is_solved(solution, board)

        self.assertEqual(True, flag)

    def test_is_solved_1(self):
        solution = [[1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]
                    ]
        board = [[1, 4, 7],
                 [2, 5, 8],
                 [3, 6, 9]
                 ]

        game = TangoGame()
        flag = game.is_solved(solution, board)

        self.assertEqual(False, flag)

    def test_get_column(self):
        solution = [[1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]
                    ]
        col0=[1,4,7]
        col1=[2,5,8]
        col2=[3,6,9]

        game = TangoGame()
        self.assertEqual(col0, game.get_column(solution,0))
        self.assertEqual(col1, game.get_column(solution, 1))
        self.assertEqual(col2, game.get_column(solution, 2))

    def test_no_breach(self):
        board=[[3, 1, 3, 1, 1, 3], [3, 3, 1, 1, 3, 1], [1, 3, 1, 3, 1, 3], [3, 1, 3, 3, 1, 1], [1, 1, 3, 1, 3, 3], [1, 3, 1, 3, 3, 1]]
        game = TangoGame()
        self.assertEqual(True, game.no_breach(board))

    def test_breach_rule2_0_1(self):
        # no piece
        game = TangoGame()
        solution = [[3, 1, 3, 1, 1, 3], [3, 3, 1, 1, 3, 1], [1, 3, 1, 3, 1, 3], [3, 1, 3, 3, 1, 1], [1, 1, 3, 1, 3, 3], [1, 3, 1, 3, 3, 1]]
        flag = game.breach_rule2(solution)
        self.assertEqual(False, flag)


    def test_breach_rule3_0_1(self):
        # no piece
        game = TangoGame()
        solution = [[3, 1, 3, 1, 1, 3], [3, 3, 1, 1, 3, 1], [1, 3, 1, 3, 1, 3], [3, 1, 3, 3, 1, 1], [1, 1, 3, 1, 3, 3], [1, 3, 1, 3, 3, 1]]
        flag = game.breach_rule3(solution)
        self.assertEqual(False, flag)