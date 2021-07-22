import pygame
import time
from pathFindingAlgorithms import *
from dataStructures import *


class Button:
    """ from https://stackoverflow.com/questions/63435298/how-to-create-a-button-class-in-pygame """

    def __init__(self, color, x, y, width, height, text=""):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(
                win,
                outline,
                (self.x - 2, self.y - 2, self.width + 4, self.height + 4),
                0,
            )

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != "":
            font = pygame.font.SysFont("comicsans", 25)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(
                text,
                (
                    self.x + (self.width / 2 - text.get_width() / 2),
                    self.y + (self.height / 2 - text.get_height() / 2),
                ),
            )

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


class GUI:
    SIZE = 600
    NUM_BOXES = 20

    def __init__(self):
        pygame.init()
        self.dis = pygame.display.set_mode((self.SIZE, self.SIZE + 50))
        self.dis.fill((255, 255, 255))
        self.state = 0
        self.colours = [
            (150, 150, 150),
            (0, 255, 0),
            (255, 0, 0),
            (50, 50, 50),
            (0, 205, 205),
            (0, 0, 255),
        ]
        pygame.display.set_caption("graphicalPathFinding")
        # create squares (playground)
        self.matrix = [
            [0 for i in range(self.NUM_BOXES)] for j in range(self.NUM_BOXES)
        ]
        self.squareSize = (self.SIZE - 10) / self.NUM_BOXES
        self.squares = [
            [
                Button(
                    (0, 0, 0),
                    5 + i * self.squareSize,
                    55 + j * self.squareSize,
                    self.squareSize - 1,
                    self.squareSize - 1,
                )
                for i in range(self.NUM_BOXES)
            ]
            for j in range(self.NUM_BOXES)
        ]
        self.buttons = [
            Button((0, 255, 0), 5, 5, self.SIZE / 4 - 5, 40, "Select start"),
            Button(
                (255, 0, 0),
                5 + self.SIZE * 1 / 4,
                5,
                self.SIZE / 4 - 5,
                40,
                "Select end",
            ),
            Button(
                (50, 50, 50),
                5 + self.SIZE * 2 / 4,
                5,
                self.SIZE / 4 - 5,
                40,
                "Lock blocks",
            ),
            Button(
                (255, 255, 0),
                5 + self.SIZE * 3 / 4,
                5,
                self.SIZE / 4 - 5,
                40,
                "Start",
            ),
        ]
        self.start, self.end = None, None
        self.path, self.order = None, None
        self.mainloop()

    def mouseClicked(self, event):
        # showcase has not started, one of the 4 buttons was clicked
        if not self.state in [4, 5, 6]:
            for i, button in enumerate(self.buttons):
                if button.isOver(event.dict["pos"]):
                    self.state = i
        # select start/end/blocked squares
        if self.state in [0, 1, 2]:
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[i])):
                    if self.squares[i][j].isOver(event.dict["pos"]):
                        # mark start/end point, if it already exists, remove the old one
                        if self.state == 0:
                            if self.start != None:
                                self.matrix[self.start[0]][
                                    self.start[1]
                                ] = 0
                            self.start = (i, j)
                        elif self.state == 1:
                            if self.end != None:
                                self.matrix[self.end[0]][self.end[1]] = 0
                            self.end = (i, j)
                        self.matrix[i][j] = self.state + 1
        # user has pressed start, now create graph and execute path finding algorithm
        elif self.state == 3:
            graph = MatrixGraph(self.NUM_BOXES, self.NUM_BOXES)
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix)):
                    if self.matrix[i][j] == 3:
                        graph.removeVertex(i, j)

            _, self.path, self.order = aStar(graph, self.start, self.end)
            self.order.pop(0)
            self.order.pop(-1)
            self.state = 4

    def mainloop(self):
        over = False
        for button in self.buttons:
            button.draw(self.dis)
        while not over:
            time.sleep(0.1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    over = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouseClicked(event)

            # graph is created and path computed, show order that vertices were visited in
            if self.state == 4:
                if len(self.order) != 0:
                    x, y = self.order.pop(0)
                    self.matrix[x][y] = 4
                else:
                    self.state = 5
            # destination vertex was visited, now show the shortest path
            elif self.state == 5:
                if len(self.path) != 1:
                    x, y = self.path.pop(0)
                    self.matrix[x][y] = 5
                else:
                    self.state = 6

            # draw squares
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[i])):
                    pygame.draw.rect(
                        self.dis,
                        self.colours[self.matrix[j][i]],
                        [
                            5 + i * self.squareSize,
                            55 + j * self.squareSize,
                            self.squareSize - 1,
                            self.squareSize - 1,
                        ],
                    )
            pygame.display.update()
        pygame.quit()