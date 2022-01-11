class IterativeDeepeningSearch:
    def __init__(self, matrix, cur, dst):
        self.matrix = matrix
        self.cur = cur
        self.dst = dst
        self.IterativeCounter = 0
        self.numberOfVisitedNodes = 0
        self.visited = [[False for j in range(20)] for i in range(20)]
        self.IterativeParent = [[(-1, -1) for j in range(20)] for i in range(20)]
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Iterative deepening search
    def iterative_search(self, limit):  # limit = Row * Column
        # global self.IterativeParent, self.directions
        for i in range(limit):
            self.visited = [[False for j in range(20)] for i in range(20)]
            self.IterativeParent = [[(-1, -1) for j in range(20)] for i in range(20)]
            if self.depth_limited_search(self.cur, i):
                for i in range(20):
                    for j in range(20):
                        if self.visited[i][j]: self.numberOfVisitedNodes += 1
                return self.numberOfVisitedNodes, self.IterativeParent, self.IterativeCounter
        return -1, self.IterativeParent, self.IterativeCounter

    # Depth limited search
    def depth_limited_search(self, current, depth):
        # global self.directions, self.visited, self.IterativeParent
        self.visited[current[0]][current[1]] = True
        self.IterativeCounter += 1
        if current == self.dst:
            return True
        if depth == 0:  # False means -> cutoff
            return False
        for k in range(4):
            nxt = (current[0] + self.directions[k][0], current[1] + self.directions[k][1])
            if 0 <= nxt[0] < 20 and 0 <= nxt[1] < 20 and self.matrix[nxt[0]][nxt[1]] != 1 and not self.visited[nxt[0]][
                nxt[1]]:
                if self.depth_limited_search(nxt, depth - 1):
                    self.IterativeParent[nxt[0]][nxt[1]] = current
                    return True
        return False

    def getPath(self):
        path_list = []
        temp = self.dst
        while temp != (-1, -1):
            path_list.append(temp)
            temp = self.IterativeParent[temp[0]][temp[1]]
        return path_list[::-1]
