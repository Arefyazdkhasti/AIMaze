class UniformCostSearch:

    def __init__(self, grid):
        self.grid = grid
        self.expandedNodeCounter = 0

    def valid(self, x, y):
        return 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0]) and self.grid[x][y] == 0

    def adjacent(self, frontier):
        dirs = [
            lambda x, y, z, p: (x, y - 1, z + 1, p + [(x, y)]),  # up
            lambda x, y, z, p: (x, y + 1, z + 1, p + [(x, y)]),  # down
            lambda x, y, z, p: (x - 1, y, z + 1, p + [(x, y)]),  # left
            lambda x, y, z, p: (x + 1, y, z + 1, p + [(x, y)]),  # right
        ]

        for (x, y, z, p) in frontier:
            for d in dirs:
                nx, ny, nz, np = d(x, y, z, p)
                if self.valid(nx, ny):
                    yield nx, ny, nz, np

    def flood(self, frontier):
        localCounter = 0
        res = list(self.adjacent(frontier))
        for (x, y, z, p) in frontier:
            self.grid[x][y] = 1
            localCounter += 1
        return res, localCounter

    def ucsShortestPath(self, start, end):
        self.expandedNodeCounter = 0
        start, end = tuple(start), tuple(end)
        frontier = [(start[0], start[1], 0, [])]
        res = []
        while frontier and self.grid[end[0]][end[1]] == 0:
            frontier, localCounter = self.flood(frontier)
            self.expandedNodeCounter += localCounter
            for (x, y, z, p) in frontier:
                if (x, y) == end:
                    res.append((z, p + [(x, y)]))
        if not res:
            return (), self.expandedNodeCounter
        return sorted(res)[0], self.expandedNodeCounter
