from pathFindingAlgorithms import *
from dataStructures import *

if __name__ == "__main__":
    graph = MatrixGraph(7, 7)
    # graph.removeVertex(0, 1)
    # graph.removeVertex(1, 1)
    # graph.removeVertex(2, 1)

    graph = aStar(graph, (3, 3), (6, 6))

    for i in range(len(graph.vertices)):
        for j in range(len(graph.vertices[i])):
            if graph.vertices[i][j] != None:
                print(graph.vertices[i][j].dist, end="\t")
            else:
                print("B", end="\t")
        print("")