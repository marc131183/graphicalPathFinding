from dataStructures import *


def heuristic(vertex1: Vertex, vertex2: Vertex):
    return ((vertex1.x - vertex2.x) ** 2 + (vertex1.y - vertex2.y) ** 2) ** 0.5
    # return abs(vertex1.x - vertex2.x) + abs(vertex1.y - vertex2.y)
    # return max(abs(vertex1.x - vertex2.x), abs(vertex1.y - vertex2.y))

def reconstructPath(solvedGraph: MatrixGraph, endCoordinates: tuple):
    way = []
    u = solvedGraph.vertices[endCoordinates[0]][endCoordinates[1]]
    while u.previous != None:
        way.append((u.previous.x, u.previous.y))
        u = u.previous

    return way

def aStar(graph: MatrixGraph, startCoordinates: tuple, endCoordinates: tuple):
    visitOrder = []

    prioQueue = BinaryMinHeap()
    startVertex = graph.vertices[startCoordinates[0]][startCoordinates[1]]
    startVertex.dist = 0
    endVertex = graph.vertices[endCoordinates[0]][endCoordinates[1]]

    prioQueue.addItem(startVertex, 0)

    while not prioQueue.isEmpty():
        u = prioQueue.extractMin()
        visitOrder.append((u.x, u.y))
        if u.x == endCoordinates[0] and u.y == endCoordinates[1]:
            return graph, reconstructPath(graph, endCoordinates), visitOrder

        for v in graph.getNeighbours(u):
            # since all weights between vertices are 1 for our case, we don't need to use weight(u, v)
            alt = u.dist + 1
            if alt < v.dist:
                v.dist = alt
                v.previous = u
                prioQueue.addItem(v, v.dist + heuristic(endVertex, v))

    return "no path found"