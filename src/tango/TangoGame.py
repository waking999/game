import pygame
import sys

import random

BKG_COLOR = pygame.Color('grey') # background color
LINE_COLOR = pygame.Color('black') # line color
LINE_WIDTH = 1  # line width

SUN = 1
MOON = 3
BLANK = 2

class TangoGame:
    def __init__(self):
        self.cWidth = self.cHeight = 100 # cell width and height
        self.rows = self.cols = 6 # row and column count on the board
        self.scale = 0.9 # shrink the character images to avoid it fully occupying each cell
        self.signScale = 0.2 # shrink the sign images to avoid it fully occupying each line

        self.pieces = self.rows * self.cols # total piece count
        self.pieces_per_character_row = self.rows // 2 # piece count per character per row
        self.pieces_per_character = self.pieces // 2 # piece count per character
        self.size = self.cWidth * self.rows, self.cHeight * self.rows # game board size

        self.piece_choices = [SUN, MOON] # piece choices

        self.board = [[BLANK] * self.cols for _ in range(self.rows)] # init a rows*cols 2d-array with BLANK filled
        self.boardClickable = [[True] * self.cols for _ in range(self.rows)] # init a rows*cols 2-array with True filled, which means all cells are clickable
        self.boardFilledCount=0 # how many cells are filled

        self.screen = pygame.display.set_mode(self.size)



        self.img_sun = pygame.image.load("../../image/sun.jpg").convert()
        self.img_moon = pygame.image.load("../../image/moon.jpg").convert()
        self.img_equal = pygame.image.load("../../image/equal.png").convert()
        self.img_cross = pygame.image.load("../../image/cross.png").convert()


    def is_3connected_bypos(self, row):
        """
        To check if 3 pieces of the same character are connected
        :param row: an array representing a row of positions of each character, generally the first and last half are for the same character individually
        :return: True, 3 or more are connected; False, less than 3 are connected
        """

        row1 = row[:self.pieces_per_character_row] # pick the first half
        row1.sort()      # sort the positions
        cnt = 1 # count of connected pieces
        for i in range(len(row1) - 1):
            if row1[i] + 1 == row1[i + 1]: # if current position is next to next position, increase the count
                cnt += 1

        return (cnt >= self.pieces_per_character_row)     # if count is larger than 3, return True

    def produce_a_solution(self):
        """
        # To produce an expected solution

        :return: a rule-satisfying solution
        """
        solution = [[BLANK] * self.rows for _ in range(self.rows)] # generate a solution full of BLANK

        for i in range(self.rows):
            row = [j for j in range(self.cols)] # generate a row of positions
            is3ConnectedFlag = True
            while is3ConnectedFlag: # only if there are 3 or more are connected
                random.shuffle(row) # shuffle the positions in each row
                is3ConnectedFlag = self.is_3connected_bypos(row) # check if there are 3 or more are connected

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

    def breach_rule1(self, solution):
        """
        To check if the solution breach rule1: either sun or moon in each cell
        :param solution: the solution produced in last step
        :return: True, a cell is neither sun nor moon; False, rule 1 is satisfied
        """
        for i in range(self.rows):
            for j in range(self.cols):
                if solution[i][j] == BLANK: # if a cell is neither sun nor moon, return True
                    return True

        # after travels all cells and we can not find the breach, return  False
        return False

    def is_3connected_byval(self, array):
        """
        To check if 3 pieces of the same character are connected
        :param row: an array representing a row of value of each character, generally the first and last half are for the same character individually
        :return: True, 3 or more are connected; False, less than 3 are connected
        """
        len1=len(array)
        for j in range(len1-2):
            if array[j]!=BLANK and array[j+1]!=BLANK and array[j+2]!=BLANK and array[j]==array[j+1] and array[j]==array[j+2]:
                return True

        return False

    def get_column(self, solution, i):
        return [row[i] for row in solution]

    def breach_rule2(self, solution):
        """
        To check if the solution breach rule2: No more than 2 characters may be next to each other, either vertically or horizontally
        :param solution: the solution produced in last step
        :return: True, 3 or more pieces of the same character are connected; False, rule 2 is satisfied
        """

        # horizontally
        len_row=len(solution)
        for i in range(len_row):
            row=solution[i]
            if self.is_3connected_byval(row):
                return True

        # vertically
        len_col=len(solution[0])
        for j in range(len_col):
            col=self.get_column(solution,j)
            if self.is_3connected_byval(col):
                return True



        # for i in range(self.rows):
        #     for j in range(self.cols): # horizontally
        #         if (((i - 2) >= 0)
        #                 and ((i - 1) >= 0)
        #                 and (solution[i][j] != BLANK)
        #                 and (solution[i - 1][j] != BLANK)
        #                 and (solution[i - 2][j] != BLANK)
        #                 and (solution[i][j] == solution[i - 1][j])
        #                 and (solution[i][j] == solution[i - 2][j])
        #         ):  # up cell
        #             return True
        #         if (((i + 2) < self.cols)
        #                 and ((i + 1) < self.cols)
        #                 and (solution[i][j] != BLANK)
        #                 and (solution[i + 1][j] != BLANK)
        #                 and (solution[i + 2][j] != BLANK)
        #                 and (solution[i][j] == solution[i + 1][j])
        #                 and (solution[i][j] == solution[i + 2][j])
        #         ):  # down cell
        #             return True
        #         if (((j - 2) >= 0)
        #                 and ((j - 1) >= 0)
        #                 and (solution[i][j] != BLANK)
        #                 and (solution[i][j - 1] != BLANK)
        #                 and (solution[i][j - 2] != BLANK)
        #                 and (solution[i][j] == solution[i][j - 1])
        #                 and (solution[i][j] == solution[i][j - 2])
        #         ):  # left cell
        #             return True
        #         if (((j + 2) < self.rows)
        #                 and ((j + 1) < self.rows)
        #                 and (solution[i][j] != BLANK)
        #                 and (solution[i][j + 1] != BLANK)
        #                 and (solution[i][j + 2] != BLANK)
        #                 and (solution[i][j] == solution[i][j + 1])
        #                 and (solution[i][j] == solution[i][j + 2])
        #         ):  # right cell
        #             return True

        return False

    def breach_rule3(self, solution):
        expectSum = (SUN + MOON) * self.rows / 2

        for i in range(self.rows):
            sum1 = sum(solution[i])
            if sum1 != expectSum:
                return True

        for j in range(self.cols):
            sum1 = 0
            for i in range(self.rows):
                sum1 += solution[i][j]
            if sum1 != expectSum:
                return True

        return False

    def init_a_solution(self):
        solution = [[BLANK] * self.cols for _ in range(self.rows)]
        isBadSolution = True

        while isBadSolution:
            solution = self.produce_a_solution()
            isBadSolution = ((self.breach_rule1(solution))
                             or (self.breach_rule2(solution))
                             or (self.breach_rule3(solution))
                             )

        return solution

    def provide_clue(self, solution, board):
        levelChoice = [0, 1, 2]  # the lower, the easier
        charShowLevels = [10, 9, 8]
        signShowLevels = [14, 13, 12]

        level = random.choice(levelChoice)

        charShowCnt = charShowLevels[level]
        signShowCnt = signShowLevels[level]

        positions = [i for i in range(self.pieces)]
        random.shuffle(positions)

        for k in range(charShowCnt):
            tmpPos = positions[k]
            i = tmpPos // self.rows
            j = tmpPos % self.rows
            board[i][j] = solution[i][j]
            self.boardClickable[i][j] = False

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

            signPos.append((d, i, j, signChar))

        return board, self.boardClickable, signPos

    def draw_board(self):
        # draw board background
        pygame.draw.rect(self.screen, BKG_COLOR, [0, 0, self.cWidth * self.cols, self.cHeight * self.rows])

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

        # draw vertical lines
        lTop = 0
        lHeight = lTop + self.cHeight * self.rows
        for c in range(self.rows):
            lLeft = c * self.cWidth
            pygame.draw.line(self.screen, LINE_COLOR, (lLeft, lTop), (lLeft, lHeight), LINE_WIDTH)

    def update_board_by_clue(self, sign_pos):
        # update images
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != BLANK:
                    left = j * self.cWidth + (self.cWidth * (1 - self.scale) + LINE_WIDTH) // 2
                    top = i * self.cHeight + (self.cHeight * (1 - self.scale) + LINE_WIDTH) // 2
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
                top = (i + 1 - self.signScale / 2) * self.cHeight
                if signChar == '=':
                    self.screen.blit(pygame.transform.scale(self.img_equal, (
                        self.cWidth * self.signScale, self.cHeight * self.signScale)),
                                     (left, top))
                elif signChar == 'x':
                    self.screen.blit(pygame.transform.scale(self.img_cross, (
                        self.cWidth * self.signScale, self.cHeight * self.signScale)),
                                     (left, top))
            elif d == 'h':
                left = (j + 1 - self.signScale / 2) * self.cWidth
                top = (i + 0.5 - self.signScale / 2) * self.cHeight

            if signChar == '=':
                self.screen.blit(pygame.transform.scale(self.img_equal,
                                                        (self.cWidth * self.signScale, self.cHeight * self.signScale)),
                                 (left, top))
            elif signChar == 'x':
                self.screen.blit(pygame.transform.scale(self.img_cross,
                                                        (self.cWidth * self.signScale, self.cHeight * self.signScale)),
                                 (left, top))

    def get_mouse_click_pos(self, pos):
        col = int(pos[0] / self.cWidth)
        row = int(pos[1] / self.cHeight)
        return col, row

    @staticmethod
    def is_solved(solution, board):
        rows = len(solution)
        cols = len(solution[0])

        for i in range(rows):
            for j in range(cols):
                if board[i][j] != solution[i][j]:
                    return False

        return True

    def show_notification(self, text, left, top):
        textSurface = self.gameFont.render(text, False, (0, 0, 0))
        self.screen.blit(textSurface, (left, top))

    def button_click(self, pos, button):

        col, row = self.get_mouse_click_pos(pos)

        if not (self.boardClickable[row][col]):
            return

        left = col * self.cWidth + (self.cWidth * (1 - self.scale) + LINE_WIDTH) // 2
        top = row * self.cHeight + (self.cHeight * (1 - self.scale) + LINE_WIDTH) // 2

        if button == 1:  # left click
            # put sun
            self.board[row][col] = SUN

            self.screen.blit(
                pygame.transform.scale(self.img_sun, (self.cWidth * self.scale, self.cHeight * self.scale)),
                (left, top))
        # elif button == 2:  # middle click
        #     board[row][col] = BLANK
        #     print(board)
        #     pygame.display.update()
        elif button == 3:  # right click
            self.board[row][col] = MOON

            self.screen.blit(
                pygame.transform.scale(self.img_moon, (self.cWidth * self.scale, self.cHeight * self.scale)),
                (left, top))

        if self.is_solved(self.solution, self.board):
            self.show_notification('Well Done!', 0, 0)

    def start(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Tango')
        self.gameFont = pygame.font.SysFont('Comic Sans MS', 30)

        # produce a solution in back end
        self.solution = self.init_a_solution()

        # generate clue
        self.board, self.boardClickable, signPos = self.provide_clue(self.solution, self.board)

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
    game = TangoGame()
    game.start()
