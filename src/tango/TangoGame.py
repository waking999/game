import pygame
import sys

import random

BKG_COLOR = pygame.Color('grey')
LINE_COLOR = pygame.Color('black')
LINE_WIDTH = 1  # line width

SUN = 1
MOON = 3
BLANK = 2



class TangoGame():
    def __init__(self):
        self.cWidth: int = 100
        self.cHeight: int = 100
        self.rows = self.cols = 6
        self.scale = 0.9
        self.signScale = 0.2


        self.pieces = self.rows * self.cols
        self.pieces_per_group_row = self.rows // 2
        self.pieces_per_group = self.pieces // 2
        self.size = self.cWidth * self.rows, self.cHeight * self.rows


        self.piece_choices = [SUN, MOON]

        self.board = [[BLANK] * self.cols for i in range(self.rows)]
        self.boardClickable = [[True] * self.cols for i in range(self.rows)]

        self.screen = pygame.display.set_mode(self.size)




        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Tango')
        self.gameFont=pygame.font.SysFont('Comic Sans MS', 30)

        self.img_sun = pygame.image.load("./image/sun.jpg").convert()
        self.img_moon = pygame.image.load("./image/moon.jpg").convert()
        self.img_equal = pygame.image.load("./image/equal.png").convert()
        self.img_cross = pygame.image.load("./image/cross.png").convert()

    def is3Connected(self, row):
        row1 = row[:(self.pieces_per_group_row)]
        row1.sort()
        cnt = 1
        for i in range(len(row1) - 1):
            if row1[i] + 1 == row1[i + 1]:
                cnt += 1

        flag = (cnt >= self.pieces_per_group_row)
        return flag

    def produceASolution(self):
        solution = [[BLANK] * self.rows for i in range(self.rows)]

        for i in range(self.rows):
            row = [j for j in range(self.cols)]
            is3ConnectedFlag = True
            while (is3ConnectedFlag):
                random.shuffle(row)
                is3ConnectedFlag = self.is3Connected(row)

            for k in range(self.cols):
                j = row[k]
                solution[i][j] = SUN if k < (self.pieces_per_group_row) else MOON

        return solution

    def breachRule1(self, solution):
        for i in range(self.rows):
            for j in range(self.cols):
                if solution[i][j] == BLANK:
                    return True

        return False

    def breachRule2(self, solution):
        for i in range(self.rows):
            for j in range(self.cols):
                if (((i - 2) >= 0)
                        and ((i - 1) >= 0)
                        and (solution[i][j] != BLANK)
                        and (solution[i - 1][j] != BLANK)
                        and (solution[i - 2][j] != BLANK)
                        and (solution[i][j] == solution[i - 1][j])
                        and (solution[i][j] == solution[i - 2][j])
                        ):  # up cell
                    return True
                if (((i + 2) < self.cols) \
                        and ((i + 1) < self.cols) \
                        and (solution[i][j] != BLANK) \
                        and (solution[i + 1][j] != BLANK) \
                        and (solution[i + 2][j] != BLANK) \
                        and (solution[i][j] == solution[i + 1][j]) \
                        and (solution[i][j] == solution[i + 2][j]) \
                        ):  # down cell
                    return True
                if (((j - 2) >= 0) \
                        and ((j - 1) >= 0) \
                        and (solution[i][j] != BLANK) \
                        and (solution[i][j - 1] != BLANK) \
                        and (solution[i][j - 2] != BLANK) \
                        and (solution[i][j] == solution[i][j - 1]) \
                        and (solution[i][j] == solution[i][j - 2]) \
                        ):  # left cell
                    return True
                if (((j + 2) < self.rows) \
                        and ((j + 1) < self.rows) \
                        and (solution[i][j] != BLANK) \
                        and (solution[i][j + 1] != BLANK) \
                        and (solution[i][j + 2] != BLANK) \
                        and (solution[i][j] == solution[i][j + 1]) \
                        and (solution[i][j] == solution[i][j + 2]) \
                        ):  # right cell
                    return True

        return False

    def breachRule3(self, solution):
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

    def initASolution(self):
        solution = [[BLANK] * self.cols for i in range(self.rows)]
        isBadSolution = True

        while (isBadSolution):
            solution = self.produceASolution()
            isBadSolution = ((self.breachRule1(solution)) \
                             or (self.breachRule2(solution)) \
                             or (self.breachRule3(solution))
                             )


        return solution

    def provideClue(self, solution, board):
        levelChoice = [0, 1, 2]  # the lower, the easier
        charShowLevels = [10, 9, 8]
        signShowLevels = [14, 13, 12]

        level=random.choice(levelChoice)

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
                d = 'h'  # compare horizonally
                i = tmpPos // (self.cols - 1)
                j = tmpPos % (self.cols - 1)
                # if (j + 1) >= self.rows:
                #     print(tmpPos, d, i, j)
                signChar = '=' if (solution[i][j] == solution[i][j + 1]) else 'x'
            else:
                tmpPos -= signs // 2
                d = 'v'  # compare vertically
                i = tmpPos // self.rows
                j = tmpPos % self.rows
                # if (i + 1) >= self.cols:
                #     print(tmpPos, d, i, j)
                signChar = '=' if (solution[i][j] == solution[i + 1][j]) else 'x'

            signPos.append((d, i, j, signChar))

        return board, self.boardClickable, signPos

    def drawBoard(self):
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

    def updateBoardByClue(self, signPos):
        # update images
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != BLANK:
                    left = j * self.cWidth + (self.cWidth * (1 - self.scale) + LINE_WIDTH) // 2
                    top = i * self.cHeight + (self.cHeight * (1 - self.scale) + LINE_WIDTH) // 2
                    if self.board[i][j] == MOON:
                        self.screen.blit(pygame.transform.scale(self.img_moon, (self.cWidth * self.scale, self.cHeight * self.scale)), (left, top))
                    else:
                        self.screen.blit(pygame.transform.scale(self.img_sun, (self.cWidth * self.scale, self.cHeight * self.scale)), (left, top))

        # udpate signs

        for d, i, j, signChar in signPos:

            if d == 'v':
                left = (j + 0.5 - self.signScale / 2) * self.cWidth
                top = (i + 1 - self.signScale / 2) * self.cHeight
                if signChar == '=':
                    self.screen.blit(pygame.transform.scale(self.img_equal, (self.cWidth * self.signScale, self.cHeight * self.signScale)),
                                     (left, top))
                elif signChar == 'x':
                    self.screen.blit(pygame.transform.scale(self.img_cross, (self.cWidth * self.signScale, self.cHeight * self.signScale)),
                                     (left, top))
            elif d == 'h':
                left = (j + 1 - self.signScale / 2) * self.cWidth
                top = (i + 0.5 -self.signScale / 2) * self.cHeight

            if signChar == '=':
                self.screen.blit(pygame.transform.scale(self.img_equal, (self.cWidth * self.signScale, self.cHeight * self.signScale)), (left, top))
            elif signChar == 'x':
                self.screen.blit(pygame.transform.scale(self.img_cross, (self.cWidth * self.signScale, self.cHeight * self.signScale)), (left, top))


    def getMouseClickPos(self, pos):
        col = int(pos[0] / self.cWidth)
        row = int(pos[1] / self.cHeight)
        return col, row

    def isSolved(sel, solution, board):
        rows = len(solution)
        cols = len(solution[0])

        for i in range(rows):
            for j in range(cols):
                if (board[i][j] != solution[i][j]):
                    return False

        return True

    def showNotification(self, text, left, top):
        textSurface = self.gameFont.render(text, False, (0, 0, 0))
        self.screen.blit(textSurface, (left, top))

    def buttonClick(self,pos, button):

        col,row = self.getMouseClickPos(pos)

        if (not (self.boardClickable[row][col])):
            return

        left = col * self.cWidth + (self.cWidth * (1 - self.scale) + LINE_WIDTH) // 2
        top = row * self.cHeight + (self.cHeight * (1 - self.scale) + LINE_WIDTH) // 2

        if button == 1:  # left click
            # put sun
            self.board[row][col] = SUN

            self.screen.blit(pygame.transform.scale(self.img_sun, (self.cWidth * self.scale, self.cHeight * self.scale)), (left, top))


        # elif button == 2:  # middle click
        #     board[row][col] = BLANK
        #     print(board)
        #     pygame.display.update()
        elif button == 3:  # right click
            self.board[row][col] = MOON

            self.screen.blit(pygame.transform.scale(self.img_moon, (self.cWidth * self.scale, self.cHeight * self.scale)), (left, top))

        if (self.isSolved(self.solution, self.board)):
            self.showNotification('Well Done!', 0, 0)

    def start(self):

        # produce a solution in back end
        self.solution = self.initASolution()

        # generate clue
        self.board, self.boardClickable, signPos = self.provideClue(self.solution, self.board)


        self.drawBoard()

        self.updateBoardByClue(signPos)


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.buttonClick(event.pos, event.button)

            pygame.display.update()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game=TangoGame()
    game.start()