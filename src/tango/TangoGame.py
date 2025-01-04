import pygame
import sys

import random

BKG_COLOR = pygame.Color('white')  # background color
LINE_COLOR = pygame.Color('black')  # line color
LINE_WIDTH = 1  # line width

SUN = 1
MOON = 3
BLANK = 2


class TangoGame:
    def __init__(self, _level=0):
        self.level = _level

        self.toolbarHeight = 50
        self.cWidth = self.cHeight = 100  # cell width and height
        self.rows = self.cols = 6  # row and column count on the board
        self.scale = 0.9  # shrink the character images to avoid it fully occupying each cell
        self.signScale = 0.2  # shrink the sign images to avoid it fully occupying each line

        self.pieces = self.rows * self.cols  # total piece count
        self.pieces_per_character_row = self.rows // 2  # piece count per character per row
        self.pieces_per_character = self.pieces // 2  # piece count per character
        self.size = self.cWidth * self.rows, self.cHeight * self.rows + self.toolbarHeight  # game board size

        self.piece_choices = [SUN, MOON]  # piece choices

        self.board = [[BLANK] * self.cols for _ in range(self.rows)]  # init a rows*cols 2d-array with BLANK filled
        self.boardClickable = [[True] * self.cols for _ in range(
            self.rows)]  # init a rows*cols 2-array with True filled, which means all cells are clickable
        self.boardFilledCount = 0  # how many cells are filled

        self.screen = pygame.display.set_mode(self.size)

        self.theme = 'CHRISTMAS'

        if self.theme == 'SUN_MOON':
            self.img_sun = pygame.image.load("../../image/sun.jpg").convert()
            self.img_moon = pygame.image.load("../../image/moon.jpg").convert()
        elif self.theme == 'CHRISTMAS':
            self.img_sun = pygame.image.load("../../image/tree.png").convert()
            self.img_moon = pygame.image.load("../../image/elf.jpg").convert()

        self.img_equal = pygame.image.load("../../image/equal.png").convert()
        self.img_cross = pygame.image.load("../../image/cross.png").convert()

    def is_3connected_bypos(self, row):
        """
        To check if 3 pieces of the same character are connected
        :param row: an array representing a row of positions of each character, generally the first and last half are for the same character individually
        :return: True, 3 or more are connected; False, less than 3 are connected
        """

        row1 = row[:self.pieces_per_character_row]  # pick the first half
        row1.sort()  # sort the positions
        cnt = 1  # count of connected pieces
        for i in range(len(row1) - 1):
            if row1[i] + 1 == row1[i + 1]:  # if current position is next to next position, increase the count
                cnt += 1

        return cnt >= self.pieces_per_character_row  # if count is larger than 3, return True

    def produce_a_solution(self):
        """
        # To produce an expected solution

        :return: a rule-satisfying solution
        """
        solution = [[BLANK] * self.rows for _ in range(self.rows)]  # generate a solution full of BLANK

        for i in range(self.rows):
            row = [j for j in range(self.cols)]  # generate a row of positions
            is3ConnectedFlag = True
            while is3ConnectedFlag:  # only if there are 3 or more are connected
                random.shuffle(row)  # shuffle the positions in each row
                is3ConnectedFlag = self.is_3connected_bypos(row)  # check if there are 3 or more are connected

            # if jump out of the while loop above, it means that we get a rule2-satisfying row
            for k in range(self.cols):
                # get the shuffled positions in each row and set up the character in the solution, we assume the first half is for sun and the last for moon
                j = row[k]
                solution[i][j] = SUN if k < self.pieces_per_character_row else MOON

        return solution

    '''
    Rules:
    1. Either Sun or Moon in each cell
    2. No more than 2 characters may be next to each other,either vertically or horizontally
    3. each row or column must contain the same number of each character
    4. cells separated by an  = sign must be of the same type
    5. Cells separated by an x sign must be of the opposite character
    '''

    def breach_rule1(self, array2d):
        """
        To check if the solution breach rule1: either sun or moon in each cell
        :param array2d: a 2d array
        :return: True, a cell is neither sun nor moon; False, rule 1 is satisfied
        """
        for i in range(self.rows):
            for j in range(self.cols):
                if array2d[i][j] == BLANK:  # if a cell is neither sun nor moon, return True
                    return True

        # after travels all cells, and we can not find the breach, return  False
        return False

    @staticmethod
    def is_3connected_byval(array):
        """
        To check if 3 pieces of the same character are connected
        :param array: an array representing a row of value of each character, generally the first and last half are for the same character individually
        :return: True, 3 or more are connected; False, less than 3 are connected
        """
        len1 = len(array)
        for j in range(len1 - 2):
            if array[j] != BLANK and array[j + 1] != BLANK and array[j + 2] != BLANK and array[j] == array[j + 1] and \
                    array[j] == array[j + 2]:
                return True

        return False

    @staticmethod
    def get_column(array_2d, i):
        """
        To get a column array out of the 2d array
        :param array_2d: a 2d array
        :param i: column index
        :return: an array
        """
        return [row[i] for row in array_2d]

    def breach_rule2(self, array2d):
        """
        To check if the solution breach rule2: No more than 2 characters may be next to each other, either vertically or horizontally
        :param array2d: a 2d array
        :return: True, 3 or more pieces of the same character are connected; False, rule 2 is satisfied
        """

        # check horizontally
        len_row = len(array2d)
        for i in range(len_row):
            row = array2d[i]
            if self.is_3connected_byval(row):
                return True

        # check vertically
        len_col = len(array2d[0])
        for j in range(len_col):
            col = self.get_column(array2d, j)
            if self.is_3connected_byval(col):
                return True

        return False

    def breach_rule3(self, array2d):
        """
        To check if the solution breach rule3: each row or column must contain the same number of each character
        :param array2d: a 2d array
        :return: True, the number of each character is not the same; False, rule 3 is satisfied
        """

        # since SUN and MOON are two positive integer, the sum of all pieces shall be always the same no matter what positions they are. Hence, we calculate the sum of them when they are of the same number.
        expectSum = (SUN + MOON) * self.rows / 2

        # check horizontally
        for i in range(self.rows):
            sum1 = sum(array2d[i])
            if sum1 != expectSum:
                return True

        # check vertically
        for j in range(self.cols):
            sum1 = 0
            for i in range(self.rows):
                sum1 += array2d[i][j]
            if sum1 != expectSum:
                return True

        return False

    def init_a_solution(self):
        """
        initialize a solution
        :return: a solution
        """

        solution = [[BLANK] * self.cols for _ in range(self.rows)]
        isBadSolution = True

        # we will continuously invoke produce_a_solution until rule 1, 2 and 3 are satisfied.
        while isBadSolution:
            solution = self.produce_a_solution()
            isBadSolution = ((self.breach_rule1(solution))
                             or (self.breach_rule2(solution))
                             or (self.breach_rule3(solution))
                             )

        return solution

    def provide_clue(self, solution, board, _level):
        """
        based on the solution, to provide some clue
        :param solution:
        :param board:
        :param _level: an integer between 0 and 3, the lower the level is, the easier the game is, the more clues the game shows
        :return: a tuple of (board, boardClickable, signPos),
                where board is updated with a few cells being filled based on the solution,
                boardClickable indicates that the filled cells can not be changed, and
                signPos contains the positions of signs satisfying rule 4 and 5.
                each signPos is a tuple of (direction: 'h','v', row index, column index, sign char: '=','x')
        """

        charShowLevels = [10, 9, 8, 7, 6]  # count choices of characters to be shown as clue
        signShowLevels = [14, 13, 12, 11, 10]  # count choices of signs to be shown as clue

        charShowCnt = charShowLevels[_level]  # get count of characters to be shown as clue
        signShowCnt = signShowLevels[_level]  # get count of signs to be shown as clue

        # to chose randomly which positions of pieces to be shown as clue
        positions = [i for i in range(self.pieces)]
        random.shuffle(positions)

        # character clue
        for k in range(charShowCnt):
            tmpPos = positions[k]
            i = tmpPos // self.rows
            j = tmpPos % self.rows
            board[i][j] = solution[i][j]
            self.boardClickable[i][j] = False  # when the position of a piece is chosen, it is unchangeable

        # there are (self.rows - 1) * self.cols positions horizontally and (self.cols - 1) * self.rows positions vertically for signs
        # to chose randomly which positions of signs to be shown as clue
        signs = (self.rows - 1) * self.cols + (self.cols - 1) * self.rows
        positions = [i for i in range(signs)]
        random.shuffle(positions)

        signPos = []
        for k in range(signShowCnt):
            tmpPos = positions[k]
            if tmpPos < signs // 2:
                d = 'h'  # compare horizontally
                i = tmpPos // (self.cols - 1)
                j = tmpPos % (self.cols - 1)
                signChar = '=' if (solution[i][j] == solution[i][j + 1]) else 'x'
            else:
                tmpPos -= signs // 2
                d = 'v'  # compare vertically
                i = tmpPos // self.rows
                j = tmpPos % self.rows
                signChar = '=' if (solution[i][j] == solution[i + 1][j]) else 'x'

            # each signPos is a tuple of (direction: h/v, row index, column index, sign char: =/x)
            signPos.append((d, i, j, signChar))

        return board, self.boardClickable, signPos

    def draw_board(self):
        """
        To draw the board
        :return: no return
        """
        # draw board background
        pygame.draw.rect(self.screen, BKG_COLOR,
                         [0, 0, self.cWidth * self.cols, self.cHeight * self.rows + self.toolbarHeight])

        # draw horizon lines
        lLeft = 0
        lWidth = lLeft + self.cWidth * self.cols
        for r in range(self.rows):
            lTop = r * self.cHeight + self.toolbarHeight
            pygame.draw.line(self.screen, LINE_COLOR, (lLeft, lTop), (lWidth, lTop), LINE_WIDTH)

        # draw vertical lines
        lTop = self.toolbarHeight
        lHeight = lTop + self.cHeight * self.rows
        for c in range(self.cols):
            lLeft = c * self.cWidth
            pygame.draw.line(self.screen, LINE_COLOR, (lLeft, lTop), (lLeft, lHeight), LINE_WIDTH)

    def update_board_by_clue(self, sign_pos):
        """
        To update the board with the clues
        :param sign_pos:
        :return: No return
        """
        # update images
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != BLANK:
                    left = j * self.cWidth + (self.cWidth * (1 - self.scale) + LINE_WIDTH) // 2
                    top = i * self.cHeight + (self.cHeight * (1 - self.scale) + LINE_WIDTH) // 2 + self.toolbarHeight
                    if self.board[i][j] == MOON:
                        self.screen.blit(pygame.transform.scale(self.img_moon,
                                                                (self.cWidth * self.scale, self.cHeight * self.scale)),
                                         (left, top))
                    else:
                        self.screen.blit(
                            pygame.transform.scale(self.img_sun, (self.cWidth * self.scale, self.cHeight * self.scale)),
                            (left, top))

        # update signs
        left = 0
        top = 0
        for d, i, j, signChar in sign_pos:

            if d == 'v':
                left = (j + 0.5 - self.signScale / 2) * self.cWidth
                top = (i + 1 - self.signScale / 2) * self.cHeight + self.toolbarHeight
            elif d == 'h':
                left = (j + 1 - self.signScale / 2) * self.cWidth
                top = (i + 0.5 - self.signScale / 2) * self.cHeight + self.toolbarHeight

            if signChar == '=':
                self.screen.blit(pygame.transform.scale(self.img_equal,
                                                        (self.cWidth * self.signScale, self.cHeight * self.signScale)),
                                 (left, top))
            elif signChar == 'x':
                self.screen.blit(pygame.transform.scale(self.img_cross,
                                                        (self.cWidth * self.signScale, self.cHeight * self.signScale)),
                                 (left, top))

    def get_mouse_click_pos(self, pos):
        """
        To get the row and column index as integers
        :param pos: the axis x,y obtained as the event of mouse click as decimals
        :return: row and column index as integers
        """
        col = int(pos[0] / self.cWidth)
        row = int((pos[1] - self.toolbarHeight) / self.cHeight)
        return row, col

    def get_center_pos(self, row, col):
        center_row = self.cHeight * (row + 0.5)
        center_col = self.cWidth * (col + 0.5)
        return center_row, center_col

    def get_centered_left_top(self, row, col):
        center_row, center_col = self.get_center_pos(row, col)
        left = center_col - self.cHeight * self.scale // 2
        top = center_row - self.cWidth * self.scale // 2
        return left, top

    @staticmethod
    def is_solved(solution, board):
        """
        To check if the board matches the expected solution
        :param solution: the solution generated
        :param board: the board the player produced
        :return: True if they match to each other; False, not matched
        """
        rows = len(solution)
        cols = len(solution[0])

        for i in range(rows):
            for j in range(cols):
                if board[i][j] != solution[i][j]:
                    return False

        return True

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

    def no_breach(self, array2d):
        isBadSolution = ((self.breach_rule1(array2d))
                         or (self.breach_rule2(array2d))
                         or (self.breach_rule3(array2d))
                         )

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

        # if this position is upon the clue cells, nothing happen
        if not (self.boardClickable[row][col]):
            return

        # get the left and top corner of the image to be shown
        left = col * self.cWidth + (self.cWidth * (1 - self.scale) + LINE_WIDTH) // 2
        top = row * self.cHeight + self.toolbarHeight + (self.cHeight * (1 - self.scale) + LINE_WIDTH) // 2

        if button == 1:  # left click
            # put sun
            self.board[row][col] = SUN
            self.screen.blit(
                pygame.transform.scale(self.img_sun, (self.cWidth * self.scale, self.cHeight * self.scale)),
                (left, top))
        elif button == 2:  # middle click
            self.board[row][col] = BLANK
            left, top = self.get_centered_left_top(row, col)
            top+=+ self.toolbarHeight
            pygame.draw.rect(self.screen, BKG_COLOR,
                             [left, top, self.cWidth * self.scale, self.cHeight * self.scale])
        elif button == 3:  # right click
            self.board[row][col] = MOON
            self.screen.blit(
                pygame.transform.scale(self.img_moon, (self.cWidth * self.scale, self.cHeight * self.scale)),
                (left, top))

        # if not (self.is_solved(self.solution, self.board)) and (self.no_breach(self.board)):
        #     print('board is not the same as the expected solution, but it is also a solution')
        #     print(self.solution)
        #     print(self.board)

        # either board=solution or board is a solution
        isSovledFlag = (self.is_solved(self.solution, self.board)) or (self.no_breach(self.board))

        if isSovledFlag:
            self.show_notification('Well Done!', 0, 0)

    def start(self):
        """
        start game
        :return: No return
        """
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Tango')
        self.gameFont = pygame.font.SysFont('Comic Sans MS', 30)

        # produce a solution in back end
        self.solution = self.init_a_solution()

        # generate clue
        self.board, self.boardClickable, signPos = self.provide_clue(self.solution, self.board, self.level)

        # draw board
        self.draw_board()

        self.update_board_by_clue(signPos)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.button_click(event.pos, event.button)

            pygame.display.update()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    levelChoice = [0, 1, 2,
                   3]  # level choices, the lower the level is, the easier the game is, the more clues the game shows

    level = random.choice(levelChoice)  # the level is randomized

    game = TangoGame(level)
    game.start()
