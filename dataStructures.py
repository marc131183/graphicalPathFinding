import math


class Node:
    def __init__(self, x: int, y: int):
        self.distance = math.inf
        self.x = x
        self.y = y
        self.parent = None


class MatrixGraph:
    def __init__(self, width: int, height: int):
        self.nodes = [[Node(x, y) for y in range(width)] for x in range(height)]

    def areNodesNeighbours(self, node1: Node, node2: Node):
        if abs(node1.x - node2.x) + abs(node1.y - node2.y) == 1:
            return True
        else:
            return False


class HeapItem:
    def __init__(self, key: int, item):
        self.key = key
        self.item = item


class BinaryMinHeap:
    def __init__(self):
        self.items = []

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
                if self.items[leftChild].key <= self.items[rightChild].key
                else rightChild
            )

    def addItem(self, item: HeapItem):
        self.items.append(item)

        currentPosition = len(self.items) - 1
        parent = self.__getParent(currentPosition)
        while parent != None:
            if self.items[parent].key > self.items[currentPosition].key:
                self.items[parent], self.items[currentPosition] = (
                    self.items[currentPosition],
                    self.items[parent],
                )
                currentPosition = parent
                parent = self.__getParent(currentPosition)
            else:
                break

    def getMin(self):
        if len(self.items) == 0:
            return None
        out = self.items[0]

        self.items[0] = self.items[-1]
        self.items.pop()

        currentPosition = 0
        successor = self.__getSmallerChild(currentPosition)
        while (
            successor != None
            and self.items[successor].key < self.items[currentPosition].key
        ):
            self.items[currentPosition], self.items[successor] = (
                self.items[successor],
                self.items[currentPosition],
            )
            currentPosition = successor
            successor = self.__getSmallerChild(currentPosition)

        return out.item