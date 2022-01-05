

class UniformCostSearch:
    def __init__(self, grid):
        self.grid = grid

    def valid(self, grid, x, y):
        return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0

    def adjacent(self, grid, frontier):
        dirs = [
            lambda x, y, z, p: (x, y - 1, z + 1, p + [(x, y)]),  # up
            lambda x, y, z, p: (x, y + 1, z + 1, p + [(x, y)]),  # down
            lambda x, y, z, p: (x - 1, y, z + 1, p + [(x, y)]),  # left
            lambda x, y, z, p: (x + 1, y, z + 1, p + [(x, y)]),  # right
        ]

        for (x, y, z, p) in frontier:
            for d in dirs:
                nx, ny, nz, np = d(x, y, z, p)
                if self.valid(grid, nx, ny):
                    yield (nx, ny, nz, np)

    def flood(self, grid, frontier):
        res = list(self.adjacent(grid, frontier))
        for (x, y, z, p) in frontier:
            grid[x][y] = 1
        return res

    def shortestPath(self, grid, start, end):
        start, end = tuple(start), tuple(end)
        frontier = [(start[0], start[1], 0, [])]
        res = []
        while frontier and grid[end[0]][end[1]] == 0:
            frontier = self.flood(grid, frontier)
            for (x, y, z, p) in frontier:
                if (x, y) == end:
                    res.append((z, p + [(x, y)]))
        if not res:
            return ()
        return sorted(res)[0]
