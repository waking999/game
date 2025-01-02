import pygame
import random
import sys

CROSS = 1
QUEEN = 3
BLANK = -1

DIRECTION_RIGHT = 0
DIRECTION_LEFT = 1
DIRECTION_UP = 2
DIRECTION_DOWN = 3

CHANCE_TIMES = 2

BKG_COLOR = pygame.Color('grey')  # background color
LINE_COLOR = pygame.Color('black')  # line color
LINE_WIDTH = 1  # line width

BACKGROUND_COLORS = ['aqua', 'blue', 'blueviolet', 'brown', 'cadetblue', 'chartreuse',
                     'chocolate', 'coral', 'crimson', 'firebrick', 'forestgreen', 'gold', 'hotpink', 'indianred']


class QueensGame:
    def __init__(self, _rows):
        self.rows = self.cols = _rows
        self.pieces = self.rows * self.cols

        self.cWidth = self.cHeight = 60  # cell width and height
        self.scale = 0.7  # shrink the character images to avoid it fully occupying each cell

        self.size = self.cWidth * self.rows, self.cHeight * self.rows  # game board size

        self.screen = pygame.display.set_mode(self.size)

        self.img_queen = pygame.image.load("../../image/queen.jpg").convert()
        self.img_cross = pygame.image.load("../../image/cross.png").convert()

        self.queens_positions_player = [BLANK for _ in range(self.rows)]

    def produce_a_queens_positions_solution(self):
        """
        # To produce an expected solution
        :return: a rule-satisfying solution
        """
        # such a producing avoids the same row and same col
        queens_positions_solution = [i for i in range(self.rows)]
        random.shuffle(queens_positions_solution)
        return queens_positions_solution

    @staticmethod
    def get_queens_positions_2d(queens_positions_solution):
        """
        To get a 2d array from 1d array
        :param queens_positions_solution:   a 1d array with index being x and value as y
        :return: a 2d array indexes as x and y
        """
        len1 = len(queens_positions_solution)
        positions_2d = []
        for i in range(len1):
            j = queens_positions_solution[i]
            positions_2d.append([i, j])

        return positions_2d

    def is_diagonally_touched(self, queens_positions):
        """
        To check if two queens are diagonally touched to each other
        :param queens_positions:
        :return: True, diagonally touched; False, no 2 queens diagonally touched
        """
        positions_2d = self.get_queens_positions_2d(queens_positions)

        len1 = len(positions_2d)

        for i in range(len1 - 1):
            c1 = positions_2d[i]
            for j in range(i, len1):
                c2 = positions_2d[j]

                if c1[0] - 1 >= 0 and c1[1] - 1 >= 0 and c1[0] - 1 == c2[0] and c1[1] - 1 == c2[
                    1]:  # one is the left top cell of another
                    return True

                if c1[0] - 1 >= 0 and c1[1] + 1 < len1 and c1[0] - 1 == c2[0] and c1[1] + 1 == c2[
                    1]:  # one is the right top cell of another
                    return True

                if c1[0] + 1 < len1 and c1[1] - 1 >= 0 and c1[0] + 1 == c2[0] and c1[1] - 1 == c2[
                    1]:  # one is the left bottom of another
                    return True

                if c1[0] + 1 < len1 and c1[1] + 1 < len1 and c1[0] + 1 == c2[0] and c1[1] + 1 == c2[
                    1]:  # one is the right bottom of another
                    return True

        return False

    @staticmethod
    def extend_color_stop(i, j, queens_positions_solution, board_color_region):
        """
        To check if stop when extending color
        :param i: the x index in the 2d array to be extended
        :param j: the y index in the 2d array to be extended
        :param queens_positions_solution: a 1d array presenting the queens positions
        :param board_color_region: a 2d array presenting the color region of each cell
        :return: True, should stop; False, no need to stop
        """
        len1 = len(queens_positions_solution)
        if i < 0 or i >= len1:  # if over left or right
            return True

        if j < 0 or j >= len1:  # if over top or bottom
            return True

        if queens_positions_solution[i] == j:  # if the cell is a queen,
            return True

        if board_color_region[i][j] != BLANK:  # if it has been colored
            return True

        return False

    @staticmethod
    def get_direction(low_chance_directions, times):
        """
        To get a direction by probability
        :param low_chance_directions: a set of which directions are of lower chance, 0:right, 1:left, 2: up, 3: down
        :param times: how high chance choices are higher than low chance choices
        :return: a direction,   0:right, 1:left, 2: up, 3: down
        """
        # 4 directions: right, left, up, down
        direction_choices = {DIRECTION_RIGHT, DIRECTION_LEFT, DIRECTION_UP, DIRECTION_DOWN}
        # except low chance directions, others are high chance directions
        high_chance_directions = direction_choices - low_chance_directions
        choices = list(
            high_chance_directions) * times  # timeing times makes high chance directions to be of truly higher chances
        choices.extend(list(low_chance_directions))
        direction = random.choice(choices)
        return direction

    def extend_color(self, i, j, direction, queens_positions_solution, board_color_region, color,
                     count_per_color_group):
        """
        extend color to the desired position
        :param i: the x index in the 2d array of the current position
        :param j: the y index in the 2d array of the current position
        :param direction: from the current position towards the direction to get to next position
        :param queens_positions_solution: a 1d array with index being x and value as y to present queens positions
        :param board_color_region: a 2d array presenting the color region of each cell
        :param color: which color to be used
        :param count_per_color_group: how many cells in each color group are colored
        :return: updated board_color_region and count_per_color_group
        """

        if direction not in [DIRECTION_RIGHT, DIRECTION_LEFT, DIRECTION_UP, DIRECTION_DOWN]:
            return board_color_region, count_per_color_group

        if direction == DIRECTION_RIGHT:  # extend to right
            next_i = i
            next_j = j + 1
        elif direction == DIRECTION_LEFT:  # extend to left
            next_i = i
            next_j = j - 1
        elif direction == DIRECTION_UP:  # extend to up
            next_i = i - 1
            next_j = j
        else:  # extend to down
            next_i = i + 1
            next_j = j

        if self.extend_color_stop(next_i, next_j, queens_positions_solution, board_color_region):
            return board_color_region, count_per_color_group

        board_color_region[next_i][next_j] = color
        count_per_color_group[color] += 1
        nextDirection = self.get_direction({DIRECTION_UP}, CHANCE_TIMES)
        board_color_region, count_per_color_group = self.extend_color(next_i, next_j, nextDirection,
                                                                      queens_positions_solution,
                                                                      board_color_region, color,
                                                                      count_per_color_group)
        return board_color_region, count_per_color_group
    #
    # @staticmethod
    # def set_color_around_single(board_color_region, i, j, not_colored_positions, count_per_color_group):
    #     """
    #     To set a single cell based on the color from a connected cell
    #     :param count_per_color_group:
    #     :param board_color_region: a 2d array presenting the color region of each cell
    #     :param i: the x index in the 2d array of the current position
    #     :param j: the y index in the 2d array of the current position
    #     :param not_colored_positions: a set of tuple (x,y) to represent which cells are not colored
    #     :return: updated board_color_region and not_colored_positions
    #     """
    #     len1 = len(board_color_region)
    #     if board_color_region[i][j] == BLANK:
    #         color_choice = set()
    #
    #         if i - 1 >= 0 and board_color_region[i - 1][j] != BLANK:  # top
    #             color_choice.add(board_color_region[i - 1][j])
    #         if j - 1 >= 0 and board_color_region[i][j - 1] != BLANK:  # left
    #             color_choice.add(board_color_region[i][j - 1])
    #         if j + 1 < len1 and board_color_region[i][j + 1] != BLANK:  # right
    #             color_choice.add(board_color_region[i][j + 1])
    #         if i + 1 < len1 and board_color_region[i + 1][j] != BLANK:  # bottom
    #             color_choice.add(board_color_region[i + 1][j])
    #
    #         if len(color_choice) > 0:  # if we can locate a color from connected cell
    #             color = random.choice(list(color_choice))  # choose a random one color to set
    #             board_color_region[i][j] = color
    #             count_per_color_group[color] += 1
    #             not_colored_positions = not_colored_positions - {
    #                 (i, j)}  # remove this position from the not_colored_positions
    #             return board_color_region, not_colored_positions, count_per_color_group
    #         else:
    #             return board_color_region, not_colored_positions, count_per_color_group
    #     else:
    #         return board_color_region, not_colored_positions, count_per_color_group

    # @staticmethod
    # def get_not_colored_positions(board_color_region):
    #     """
    #     To get the positions which are not colored
    #     :param board_color_region: a 2d array presenting the color region of each cell
    #     :return: a set of tuple (x,y) representing uncolor the positions
    #     """
    #     len1 = len(board_color_region)
    #     not_colored_positions = set()
    #     for i in range(len1):
    #         for j in range(len1):
    #             if board_color_region[i][j] == BLANK:
    #                 not_colored_positions.add((i, j))
    #     return not_colored_positions

    # def set_color_around(self, board_color_region, count_per_color_group):
    #     """
    #     To set color on the whole board
    #     :param count_per_color_group:
    #     :param board_color_region: a 2d array presenting the color region of each cell
    #     :return: updated board_color_region
    #     """
    #     # get a set of uncolored positions
    #     not_colored_positions = self.get_not_colored_positions(board_color_region)
    #
    #     # pick a position from not_colored_positions, color it until all positions are colored
    #     while len(not_colored_positions) > 0:
    #         i, j = random.choice(list(not_colored_positions))
    #         board_color_region, not_colored_positions, count_per_color_group = self.set_color_around_single(
    #             board_color_region, i, j,
    #             not_colored_positions, count_per_color_group)
    #
    #     return board_color_region, count_per_color_group

    # def set_color_around_1round(self, board_color_region, count_per_color_group):
    #     not_colored_positions = self.get_not_colored_positions(board_color_region)
    #
    #     count = int(0.1 * len(not_colored_positions))
    #     while count > 0:
    #         count -= 1
    #         i, j = random.choice(list(not_colored_positions))
    #         board_color_region, not_colored_positions, count_per_color_group = self.set_color_around_single(
    #             board_color_region, i, j,
    #             not_colored_positions, count_per_color_group)
    #
    #     return board_color_region

    @staticmethod
    def set_color_around_color(board_color_region, count_per_color_group, color):
        """

        :param board_color_region:
        :param count_per_color_group:
        :param color:
        :return:
        """
        len1 = len(board_color_region)
        for i in range(len1):
            for j in range(len1):
                if board_color_region[i][j] == color:
                    if i - 1 > 0 and board_color_region[i - 1][j] == BLANK:  # up
                        board_color_region[i - 1][j] = color
                        count_per_color_group[color] += 1
                    if i + 1 < len1 and board_color_region[i + 1][j] == BLANK:  # down
                        board_color_region[i + 1][j] = color
                        count_per_color_group[color] += 1
                    if j - 1 > 0 and board_color_region[i][j - 1] == BLANK:  # left
                        board_color_region[i][j - 1] = color
                        count_per_color_group[color] += 1
                    if j + 1 < len1 and board_color_region[i][j + 1] == BLANK:  # down
                        board_color_region[i][j + 1] = color
                        count_per_color_group[color] += 1

        return board_color_region, count_per_color_group

    def set_color_around_for_small_color_group(self, board_color_region, count_per_color_group):
        """

        :param board_color_region:
        :param count_per_color_group:
        :return:
        """
        vault = 2
        len1 = len(count_per_color_group)
        for color in range(len1):
            if count_per_color_group[color] <= vault:
                board_color_region, count_per_color_group = self.set_color_around_color(board_color_region,
                                                                                        count_per_color_group, color)

        return board_color_region, count_per_color_group

    def get_board_color_region(self, queens_positions_solution):
        """
        To set color region on the board according to queens_positions
        :param queens_positions_solution: a 1d array with index being x and value as y to present queens positions
        :return: board_color_region, a 2d array presenting the color region of each cell
        """
        # initialize board_color_region with illegal color
        board_color_region = [[BLANK] * self.cols for _ in range(self.rows)]

        # start from a random color group
        color_group = [i for i in range(self.rows)]
        random.shuffle(color_group)
        # set color based on each queen group

        count_per_color_group = [0 for _ in range(self.rows)]

        for i in color_group:  # each row has only one queen, each queen has only one color, so row and color can be 1:1 mapped
            j = queens_positions_solution[i]

            low_chance_choices = set()
            if i == 0:
                low_chance_choices = {DIRECTION_UP}
            elif i == self.rows - 1:
                low_chance_choices = {DIRECTION_DOWN}

            direction = self.get_direction(low_chance_choices, CHANCE_TIMES)
            board_color_region[i][j] = i
            count_per_color_group[i] += 1
            board_color_region, count_per_color_group = self.extend_color(i, j, direction,
                                                                          queens_positions_solution,
                                                                          board_color_region,
                                                                          i,
                                                                          count_per_color_group)

        print('set color based on queen group')
        print(board_color_region)
        print(count_per_color_group)

        # set color based on around
        # board_color_region = self.set_color_around(board_color_region)
        # board_color_region = self.set_color_around_1round(board_color_region)
        # print('set color based on around')
        # print(board_color_region)

        # set color based on around color
        board_color_region, count_per_color_group = self.set_color_around_for_small_color_group(board_color_region,
                                                                                                count_per_color_group)
        print('set color based on around color')
        print(board_color_region)
        print(count_per_color_group)

        return board_color_region

    def init_a_solution(self):
        """
        initialize a solution
        :return: a solution
        """
        queens_positions_solution = [i for i in range(self.rows)]

        isBadSolution = True
        # we will continuously invoke produce_a_solution until no diagonally touched and in the same color region
        while isBadSolution:
            queens_positions_solution = self.produce_a_queens_positions_solution()
            isBadSolution = self.is_diagonally_touched(queens_positions_solution)

        return queens_positions_solution

    """
    1. exactly one queen in each row, column and color region
    2. two queens cannot touch each other, not even diagonally
    """

    def draw_board(self):
        """
        To draw the board
        :return: no return
        """
        # draw board background
        pygame.draw.rect(self.screen, BKG_COLOR, [0, 0, self.cWidth * self.cols, self.cHeight * self.rows])

        for i in range(self.rows):
            for j in range(self.cols):
                if self.board_color_region[i][j] != BLANK:
                    color = BACKGROUND_COLORS[self.board_color_region[i][j]]
                    pygame.draw.rect(self.screen, color,
                                     [j * self.cWidth, i * self.cHeight, self.cWidth, self.cHeight])

        # draw horizon lines
        lLeft = 0
        lWidth = lLeft + self.cWidth * self.cols
        for r in range(self.rows):
            lTop = r * self.cHeight
            pygame.draw.line(self.screen, LINE_COLOR, (lLeft, lTop), (lWidth, lTop), LINE_WIDTH)

        # draw vertical lines
        lTop = 0
        lHeight = lTop + self.cHeight * self.rows
        for c in range(self.cols):
            lLeft = c * self.cWidth
            pygame.draw.line(self.screen, LINE_COLOR, (lLeft, lTop), (lLeft, lHeight), LINE_WIDTH)

    def get_mouse_click_pos(self, pos):
        """
        To get the row and column index as integers
        :param pos: the axis x,y obtained as the event of mouse click as decimals
        :return: row and column index as integers
        """
        col = int(pos[0] / self.cWidth)
        row = int(pos[1] / self.cHeight)
        return row, col

    def show_notification(self, text, left, top):
        """
        To show notification
        :param text: the content of the notification
        :param left: left position of the start of the notification
        :param top: top position of the start of the notification
        :return:
        """
        textSurface = self.gameFont.render(text, False, (0, 0, 0))
        self.screen.blit(textSurface, (left, top))

    def get_center_pos(self, row, col):
        center_row = self.cHeight * (row + 0.5)
        center_col = self.cWidth * (col + 0.5)
        return center_row, center_col

    def get_centered_left_top(self, row, col):
        center_row, center_col = self.get_center_pos(row, col)
        left = center_col - self.cHeight * self.scale // 2
        top = center_row - self.cWidth * self.scale // 2
        return left, top

    def is_solved(self):
        return self.queens_positions_solution == self.queens_positions_player

    @staticmethod
    def is_blank(array_1d):
        for v in array_1d:
            if v == BLANK:
                return True

        return False

    @staticmethod
    def is_same_col(array_1d):
        len1 = len(array_1d)
        for i in range(len1 - 1):
            for j in range(i + 1, len1):
                if array_1d[i] == array_1d[j]:
                    return True

        return False

    @staticmethod
    def is_same_color(array_1d, board_color_region):
        len1 = len(array_1d)
        for i1 in range(len1 - 1):
            j1 = array_1d[i1]
            for i2 in range(i1 + 1, len1):
                j2 = array_1d[i2]
                if board_color_region[i1][j1] == board_color_region[i2][j2]:
                    return True

        return False

    def is_a_solution(self):
        isBadSolution = ((self.is_blank(self.queens_positions_player))  # is blank
                         or (self.is_same_col(self.queens_positions_player))  # is in same column
                         or (self.is_diagonally_touched(self.queens_positions_player))  # is diagonally touched
                         or (self.is_same_color(self.queens_positions_player, self.board_color_region))
                         # is in the same color region
                         )
        if not isBadSolution:
            print(self.queens_positions_player)

        return not isBadSolution

    def button_click(self, pos, button):
        """
        To respond upon the button click event
        :param pos: the position of the button click
        :param button: which button is clicked
        :return:  No return
        """

        # get row and col index of the cell where the mouse button is clicked
        row, col = self.get_mouse_click_pos(pos)

        # get the left and top corner of the image to be shown
        left, top = self.get_centered_left_top(row, col)

        if button == 1:  # left click: cross
            # put cross
            self.screen.blit(
                pygame.transform.scale(self.img_cross, (self.cWidth * self.scale, self.cHeight * self.scale)),
                (left, top))
        elif button == 2:  # middle click
            if self.board_color_region[row][col] != BLANK:
                color = BACKGROUND_COLORS[self.board_color_region[row][col]]
            else:
                color = BKG_COLOR

            left, top = self.get_centered_left_top(row, col)
            pygame.draw.rect(self.screen, color,
                             [left, top, self.cWidth * self.scale, self.cHeight * self.scale])
        elif button == 3:  # right click
            # put queen
            self.queens_positions_player[row] = col
            self.screen.blit(
                pygame.transform.scale(self.img_queen, (self.cWidth * self.scale, self.cHeight * self.scale)),
                (left, top))

        print(self.queens_positions_player)
        # either board=solution or board is a solution
        is_solved_flag = ((self.is_solved())
                          or (self.is_a_solution())
                          )

        if is_solved_flag:
            self.show_notification('Well Done!', 0, 0)

    def start(self):
        """
        start game
        :return: No return
        """

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Queens')
        self.gameFont = pygame.font.SysFont('Comic Sans MS', 30)

        # produce a solution in back end
        self.queens_positions_solution = self.init_a_solution()
        print(self.queens_positions_solution)

        self.board_color_region = self.get_board_color_region(self.queens_positions_solution)
        # print(self.board_color_region)

        # draw board
        self.draw_board()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.button_click(event.pos, event.button)

            pygame.display.update()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    rowsChoices = [8, 9, 10, 11, 12]
    rows = random.choice(rowsChoices)

    game = QueensGame(rows)
    game.start()
