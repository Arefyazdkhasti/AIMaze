import heapq


class AStar:

    def __init__(self, matrix):
        self.matrix = matrix

    expandNodeCounter = 0
    visited = {}

    @staticmethod
    def heuristicFunction(dst, i, j):
        return abs(dst[0] - i) + abs(dst[1] - j)

    def aStar(self, src, dst):
        global expandNodeCounter, visited
        expandNodeCounter = 0

        width = len(self.matrix[0])
        height = len(self.matrix)

        frontier = [(self.heuristicFunction(dst, src[0], src[1]), (src[0], src[1]), list(), 0,
                     self.heuristicFunction(dst, src[0], src[1]))]
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
                return path, expandNodeCounter
            # set the cost (path is enough since the heuristic won't change)
            visited[(i, j)] = state[3]
            # explore neighbor
            # change > 0 to < 1 in order to use binary matrix 0
            neighbor = list()
            if i > 0 and self.matrix[i - 1][j] < 1:  # top
                neighbor.append((i - 1, j))
            if i < height - 1 and self.matrix[i + 1][j] < 1:
                neighbor.append((i + 1, j))
            if j > 0 and self.matrix[i][j - 1] < 1:
                neighbor.append((i, j - 1))
            if j < width - 1 and self.matrix[i][j + 1] < 1:
                neighbor.append((i, j + 1))

            for n in neighbor:
                next_cost = state[3] + 1
                if n in visited and visited[n] < next_cost:
                    continue
                heapq.heappush(frontier, (
                    self.heuristicFunction(dst, n[0], n[1]) + next_cost, n, [state[1]] + state[2], next_cost,
                    self.heuristicFunction(dst, n[0], n[1])))
                expandNodeCounter += 1

        if state[0] != dst:
            return path, expandNodeCounter
