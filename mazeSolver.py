import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from UniformCostSearch import UniformCostSearch

filePath = "C:/Users/Acer/IdeaProjects/AIProject/generated_maze.txt"

with open(filePath, "r") as file:
    matrix = [
        [x for x in line.split()]
        for line in file
    ]

for row in matrix:
    print(row)

shit = [[0 for x in range(20)] for y in range(20)]

for row in range(0, 20):
    for col in range(0, 20):
        if matrix[row][col] == '-' or matrix[row][col] == 'F' or matrix[row][col] == 'A':
            shit[row][col] = 1
        elif matrix[row][col] == 'W':
            shit[row][col] = 0

for row in shit:
    print(row)

G = nx.from_numpy_matrix(np.array(shit))
nx.draw(G, with_labels=True)

graph = dict()

'''
# به ازای هر نود مقصدهای اون نود رو توی ارایه way_list دخیره میکنیم و داخل دیکشنری graph میریزیم
for i in nx.nodes(G):
    way_list = []
    for j in range(0, len(nx.edges(G, i))):
        # nx.edges(G, i) لیست نودهای مقصد از نود i را میدهد. سپس از آن ارایه j امین خانه اش که شامل یک دوتایی مبدا و
        # مقصد هس رو میگیریم و از اون هم 1 که شماره مقصد به تنهایی هست رو دریافت میکنیم
        way_list.append(list(nx.edges(G, i))[j][1])
    way_list.sort()
    graph[i] = way_list

for i in graph:
    print(i, graph[i])
'''

for i in range(0, 20):
    for j in range(0, 20):
        if matrix[i][j] != 'W':
            neighbors = []
            if j - 1 >= 0:
                if matrix[i][j - 1] != 'W':
                    neighbors.append(20 * i + j - 1)
            if j + 1 < 20:
                if matrix[i][j + 1] != 'W':
                    neighbors.append(20 * i + j + 1)
            if i + 1 < 20:
                if matrix[i + 1][j] != 'W':
                    neighbors.append(20 * (i + 1) + j)
            if i - 1 >= 0:
                if matrix[i - 1][j] != 'W':
                    neighbors.append(20 * (i - 1) + j)
        else:
            neighbors = []
        graph[i * 20 + j] = neighbors

for i in graph:
    print(i, graph[i])


# plt.show()

def dfs(adj_list, start, target, path, visited=set()):
    path.append(start)
    visited.add(start)
    if start == target:
        return path
    for neighbour in adj_list[start]:
        if neighbour not in visited:
            result = dfs(adj_list, neighbour, target, path, visited)
            if result is not None:
                return result
            path.pop()
    return None


traversal_path = []
dfs(graph, 0, 66, traversal_path)
print(traversal_path)

path = list()


'''

def DFS(currentNode, destination, graph, maxDepth, curList):
    #print("Checking for destination", currentNode)
    curList.append(currentNode)
    if currentNode == destination:
        return True
    if maxDepth <= 0:
        path.append(curList)
        return False
    for node in graph[currentNode]:
        if DFS(node, destination, graph, maxDepth - 1, curList):
            return True
        else:
            curList.pop()
    return False


def iterativeDDFS(currentNode, destination, graph, maxDepth):
    for i in range(maxDepth):
        curList = list()
        if DFS(currentNode, destination, graph, i, curList):
            return True
    return False


if not iterativeDDFS(0, 66, graph,20):
    print("Path is not available")
else:
    print("A path exists")
    print(path.pop())

if not iterativeDDFS(66, 315 , graph,20):
    print("Path is not available")
else:
    print("A path exists")
    print(path.pop())


# UFS
dirs = [
    lambda x, y, z, p: (x, y - 1, z + 1, p + [(x, y)]),  # up
    lambda x, y, z, p: (x, y + 1, z + 1, p + [(x, y)]),  # down
    lambda x, y, z, p: (x - 1, y, z + 1, p + [(x, y)]),  # left
    lambda x, y, z, p: (x + 1, y, z + 1, p + [(x, y)]),  # right
]


def valid(grid, x, y):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0


def adjacent(grid, frontier):
    for (x, y, z, p) in frontier:
        for d in dirs:
            nx, ny, nz, np = d(x, y, z, p)
            if valid(grid, nx, ny):
                yield (nx, ny, nz, np)


def flood(grid, frontier):
    res = list(adjacent(grid, frontier))
    for (x, y, z, p) in frontier:
        grid[x][y] = 1
    return res


def shortest(grid, start, end):
    start, end = tuple(start), tuple(end)
    frontier = [(start[0], start[1], 0, [])]
    res = []
    while frontier and grid[end[0]][end[1]] == 0:
        frontier = flood(grid, frontier)
        for (x, y, z, p) in frontier:
            if (x, y) == end:
                res.append((z, p + [(x, y)]))
    if not res:
        return ()
    return sorted(res)[0]


# UCS
path1 = shortest(shit, (0, 0), (3, 6))
path2 = shortest(shit, (3, 6), (15, 15))
total_cost = path1[0] + path2[0]
final_path = list(path1[1] + path2[1])
print("Uniform Cost Search: \n")
print("shortest cost to 2 fruits: " + str(total_cost))
print("shortest path to 2 fruits: ")
# (3,6) appeared twice
final_path.remove((3, 6))
print(final_path)


current_x = 0
current_y = 0
# all four possible neighbors for each node store in this list

for i in range(0, 20):
    for j in range(0, 20):
        neighbors = []
        if j - 1 >= 0:
            neighbors.append([i, j - 1])
        if j + 1 < 20:
            neighbors.append([i, j + 1])
        if i + 1 < 20:
            neighbors.append([i + 1, j])
        if i - 1 >= 0:
            neighbors.append([i - 1, j])
        print(str(i) + " " + str(j))
        print(neighbors)

        for neighbor in neighbors:
            if matrix[neighbor[0]][neighbor[1]] == '-':
                current_x = neighbor[0]
                current_y = neighbor[1]
                break
            elif matrix[neighbor[0]][neighbor[1]] == 'F':
                current_x = neighbor[0]
                current_y = neighbor[1]
                print("__________________________Pashmam__________________________")
                break

        i = current_x
        j = current_y
        print("new spot:" + str(i) + " " + str(j))

'''
