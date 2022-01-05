import heapq


class AStar:

    def __init__(self, matrix):
        self.matrix = matrix

    counter = 0
    visited = {}

    def heuristic(self, dst, i, j):
        return abs(dst[0] - i) + abs(dst[1] - j)

    def aStar(self, src, dst, matrix):
        global counter, visited
        counter = 0

        width = len(matrix[0])
        height = len(matrix)

        # small variation for easier code, state is (coord_tuple, previous, path_cost, heuristic_cost)
        frontier = [
            (self.heuristic(dst, src[0], src[1]), (src[0], src[1]), list(), 0, self.heuristic(dst, src[0], src[1]))]
        heapq.heapify(frontier)
        visited = {}
        state = 0
        path = []

        while len(frontier):
            # get first state (least cost)
            state = heapq.heappop(frontier)

            # goal check
            (i, j) = state[1]
            if (i, j) == (dst[0], dst[1]):
                path = [state[1]] + state[2]
                path.reverse()
                return path
            # set the cost (path is enough since the heuristic won't change)
            visited[(i, j)] = state[3]
            # explore neighbor
            neighbor = list()
            if i > 0 and matrix[i - 1][j] > 0:  # top
                neighbor.append((i - 1, j))
            if i < height - 1 and matrix[i + 1][j] > 0:
                neighbor.append((i + 1, j))
            if j > 0 and matrix[i][j - 1] > 0:
                neighbor.append((i, j - 1))
            if j < width - 1 and matrix[i][j + 1] > 0:
                neighbor.append((i, j + 1))

            for n in neighbor:
                next_cost = state[3] + 1
                if n in visited and visited[n] < next_cost:
                    continue
                heapq.heappush(frontier, (
                    self.heuristic(dst, n[0], n[1]) + next_cost, n, [state[1]] + state[2], next_cost,
                    self.heuristic(dst, n[0], n[1])))
                counter += 1

        if state[0] != dst:
            return path


    '''
    src = (0, 0)
    dst = (3, 6)

    path = self.aStar(matrix)

    if len(path) != 0:
        print("path1 is:")
        print(path, "\n")
        print("cost of shortest path1 is:\t", len(path))
        print("number of expanded node is:\t", counter)

        aStar_traversal1 = []
        for item in path:
            item = item[0] * 20 + item[1]
            aStar_traversal1.append(item)


    else:
        print("shortest path doesn't exist")

    src = (3, 6)
    dst = (15, 15)

    path = aStar(matrix)

    if len(path) != 0:
        print("path2 is:")
        print(path, "\n")
        print("cost of shortest path2 is:\t", len(path))
        print("number of expanded node is:\t", counter)

        aStar_traversal2 = []
        for item in path:
            item = item[0] * 20 + item[1]
            aStar_traversal2.append(item)'''

    # printMatrixWithPath("A *", matrix, aStar_traversal1 + aStar_traversal2)
