

class UniformCostSearch:

    expandedNodeCounter = 0

    def __init__(self, grid):
        self.grid = grid

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
                if self.valid( nx, ny):
                    yield (nx, ny, nz, np)

    def flood(self, frontier):
        global expandedNodeCounter
        expandedNodeCounter = 0
        res = list(self.adjacent(frontier))
        for (x, y, z, p) in frontier:
            self.grid[x][y] = 1
            expandedNodeCounter += 1
        return res, expandedNodeCounter

    def ucsShortestPath(self, start, end):
        global expandedNodeCounter
        expandedNodeCounter = 0
        start, end = tuple(start), tuple(end)
        frontier = [(start[0], start[1], 0, [])]
        res = []
        while frontier and self.grid[end[0]][end[1]] == 0:
            frontier, expandedNodes = self.flood(frontier)
            expandedNodeCounter += expandedNodes
            for (x, y, z, p) in frontier:
                if (x, y) == end:
                    res.append((z, p + [(x, y)]))
        if not res:
            return (), expandedNodeCounter
        return sorted(res)[0], expandedNodeCounter
