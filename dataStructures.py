import math


class Vertex:
    def __init__(self, x: int, y: int):
        self.dist = math.inf
        self.x = x
        self.y = y
        self.previous = None


class MatrixGraph:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.vertices = [[Vertex(x, y) for y in range(width)] for x in range(height)]
        # -1 means that there is no edge between vertices, 0 that it's the same vertex and 1 if there is an edge
        self.edges = [
            [-1 for y in range(width * height)] for x in range(width * height)
        ]
        self.combinations = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        ]#(1, 1), (1, -1), (-1, 1), (-1, -1)
        for i in range(len(self.edges)):
            self.edges[i][i] = 0
            x, y = self.convertSingletoXY(i)
            for comb in self.combinations:
                if self.isInsideMatrix(x + comb[0], y + comb[1]):
                    self.edges[i][self.convertXYtoSingle(x + comb[0], y + comb[1])] = 1

    def isInsideMatrix(self, x: int, y: int):
        if x < len(self.vertices) and x >= 0 and y < len(self.vertices[x]) and y >= 0:
            return True
        else:
            return False

    def convertXYtoSingle(self, x: int, y: int):
        return x * self.width + y

    def convertSingletoXY(self, single: int):
        return math.floor(single / self.width), single % self.width

    def getNeighbours(self, vertex: Vertex):
        indices = [
            index
            for index, element in enumerate(
                self.edges[self.convertXYtoSingle(vertex.x, vertex.y)]
            )
            if element == 1
        ]
        indices = [self.convertSingletoXY(single) for single in indices]
        neighbours = [self.vertices[elem[0]][elem[1]] for elem in indices]
        return neighbours

    def removeVertex(self, x: int, y: int):
        single = self.convertXYtoSingle(x, y)
        self.vertices[x][y] = None
        for i in range(len(self.edges)):
            self.edges[single][i] = -1
            self.edges[i][single] = -1
            self.edges[single][single] = 0

    def addVertex(self, x: int, y: int):
        single = self.convertXYtoSingle(x, y)
        self.vertices[x][y] = Vertex(x, y)
        self.edges[single][single] = 0
        for comb in self.combinations:
            new_x, new_y = x + comb[0], y + comb[1]
            if (
                self.isInsideMatrix(new_x, new_y)
                and self.vertices[new_x][new_y] != None
            ):
                self.edges[self.convertXYtoSingle(x, y)][
                    self.convertXYtoSingle(new_x, new_y)
                ] = 1
                self.edges[self.convertXYtoSingle(new_x, new_y)][
                    self.convertXYtoSingle(x, y)
                ] = 1


class BinaryMinHeap:
    def __init__(self):
        self.items = []
        self.priorityDictionary = {}

    def __getPriority(self, vertex: Vertex):
        return self.priorityDictionary[(vertex.x, vertex.y)]

    def isEmpty(self):
        return len(self.items) == 0

    def __getParent(self, position: int):
        if position == 0:
            return None
        else:
            return math.ceil(position / 2) - 1

    def __getLeftChild(self, position: int):
        if position * 2 + 1 >= len(self.items):
            return None
        else:
            return position * 2 + 1

    def __getRightChild(self, position: int):
        if position * 2 + 2 >= len(self.items):
            return None
        else:
            return position * 2 + 2

    def __getSmallerChild(self, position: int):
        leftChild = self.__getLeftChild(position)
        rightChild = self.__getRightChild(position)
        if leftChild == None:
            return None
        elif rightChild == None:
            return self.__getLeftChild(position)
        else:
            return (
                leftChild
                if self.__getPriority(self.items[leftChild])
                <= self.__getPriority(self.items[rightChild])
                else rightChild
            )

    def addItem(self, vertex: Vertex, priority: int):
        self.priorityDictionary[(vertex.x, vertex.y)] = priority
        self.items.append(vertex)

        currentPosition = len(self.items) - 1
        parent = self.__getParent(currentPosition)
        while parent != None:
            if self.__getPriority(self.items[parent]) > self.__getPriority(
                self.items[currentPosition]
            ):
                self.items[parent], self.items[currentPosition] = (
                    self.items[currentPosition],
                    self.items[parent],
                )
                currentPosition = parent
                parent = self.__getParent(currentPosition)
            else:
                break

    def extractMin(self):
        if self.isEmpty():
            return None
        out = self.items[0]

        self.items[0] = self.items[-1]
        self.items.pop()

        currentPosition = 0
        successor = self.__getSmallerChild(currentPosition)
        while successor != None and self.__getPriority(
            self.items[successor]
        ) < self.__getPriority(self.items[currentPosition]):
            self.items[currentPosition], self.items[successor] = (
                self.items[successor],
                self.items[currentPosition],
            )
            currentPosition = successor
            successor = self.__getSmallerChild(currentPosition)

        return out