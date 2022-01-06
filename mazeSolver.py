from colorama import Fore
from Astar import AStar
from UniformCostSearch import UniformCostSearch
from IterativeDeepeningSearch import IterativeDeepeningSearch

filePath = "generated_maze.txt"

with open(filePath, "r") as file:
    matrix = [
        [x for x in line.split()]
        for line in file
    ]

for row in matrix:
    print(row)

binaryMatrix1 = [[0 for x in range(20)] for y in range(20)]
binaryMatrix0 = [[0 for x in range(20)] for y in range(20)]

for row in range(0, 20):
    for col in range(0, 20):
        if matrix[row][col] == '-' or matrix[row][col] == 'F' or matrix[row][col] == 'A':
            binaryMatrix1[row][col] = 1
            binaryMatrix0[row][col] = 0
        elif matrix[row][col] == 'W':
            binaryMatrix1[row][col] = 0
            binaryMatrix0[row][col] = 1

binaryMatrixBackUp = binaryMatrix0

for row in binaryMatrix0:
    print(row)


graph = dict()

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

# for i in graph:
#    print(i, graph[i])


# plt.show()

ids = IterativeDeepeningSearch(binaryMatrix1, (0,0), (3,6))
numberOfVisitedNodes, IterativeParent, IterativeCounter = ids.iterative_search(400)
path_list = ids.getPath()
print ("--")
print(path_list)
print(numberOfVisitedNodes)
print(IterativeParent)
print(IterativeCounter)
print ("--")



def printMatrixWithPath(algorithm_name, _matrix, path, expandedNodes = 0):
    print("--------------------- Algorithm: ", algorithm_name + " ---------------------")
    for row in range(0, len(_matrix)):
        for col in range(0, len(_matrix)):
            if 20 * row + col in path:
                _matrix[row][col] = "*"

    for row in range(0, len(_matrix)):
        for col in range(0, len(_matrix)):
            if _matrix[row][col] == "*":
                print("*", end=" ")
            elif _matrix[row][col] == "W":
                print("W", end=" ")
            else:
                print(_matrix[row][col], end=" ")
        print()

    print("Path is: ", path)
    print("Cost is: ", len(path))
    path.clear()

# region UFS


ucs = UniformCostSearch(binaryMatrix0)
path1 = ucs.shortestPath(binaryMatrix0, (0, 0), (3, 6))
path2 = ucs.shortestPath(binaryMatrix0, (3, 6), (15, 15))
total_cost = path1[0] + path2[0]
final_path = list(path1[1] + path2[1])
# (3,6) appeared twice
final_path.remove((3, 6))
print(final_path)

traversal = []
for item in final_path:
    item = item[0] * 20 + item[1]
    traversal.append(item)

print(traversal)
matrix_USF = matrix
printMatrixWithPath("Uniform Cost Search", matrix_USF, traversal)
# endregion

# A*
src1 = (0, 0)
dst1 = (3, 6)
aStar = AStar(binaryMatrix1)
path1 = aStar.aStar(src1, dst1, binaryMatrix1)

if len(path1) != 0:

    aStar_traversal1 = []
    for item in path1:
        item = item[0] * 20 + item[1]
        aStar_traversal1.append(item)
else:
    print("shortest path doesn't exist")

src2 = (3, 6)
dst2 = (15, 15)
aStar = AStar( binaryMatrix1)
path2 = aStar.aStar(src2, dst2, binaryMatrix1)

if len(path2) != 0:

    aStar_traversal2 = []
    for item in path2:
        item = item[0] * 20 + item[1]
        aStar_traversal2.append(item)
else:
    print("shortest path doesn't exist")

final_path = list(aStar_traversal1 + aStar_traversal2)
# 66 appear twice in the list one for dst of path1 and two for src of path2
final_path.remove(66)
matrix_AStar = matrix
printMatrixWithPath("A *", matrix_AStar, final_path)
# endregion


'''
# IDDFS
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


----------------------------------------
# DFS
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


# traversal_path = []
# dfs(graph, 0, 66, traversal_path)
# print(traversal_path)
----------------------------------------


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
                break

        i = current_x
        j = current_y
        print("new spot:" + str(i) + " " + str(j))
----------------------------------------


# Graph
G = nx.from_numpy_matrix(np.array(shit1))
nx.draw(G, with_labels=True)

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
----------------------------------------
    
# region A*
counter = 0
visited = {}


def heuristic(i, j):
    return abs(dst[0] - i) + abs(dst[1] - j)


def astar(binaryMatrixBackUp):
    global counter, visited
    counter = 0

    width = len(binaryMatrixBackUp[0])
    height = len(binaryMatrixBackUp)

    # small variation for easier code, state is (coord_tuple, previous, path_cost, heuristic_cost)
    frontier = [(heuristic(src[0], src[1]), (src[0], src[1]), list(), 0, heuristic(src[0], src[1]))]
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
        if i > 0 and binaryMatrixBackUp[i - 1][j] > 0:  # top
            neighbor.append((i - 1, j))
        if i < height - 1 and binaryMatrixBackUp[i + 1][j] > 0:
            neighbor.append((i + 1, j))
        if j > 0 and binaryMatrixBackUp[i][j - 1] > 0:
            neighbor.append((i, j - 1))
        if j < width - 1 and binaryMatrixBackUp[i][j + 1] > 0:
            neighbor.append((i, j + 1))

        for n in neighbor:
            next_cost = state[3] + 1
            if n in visited and visited[n] < next_cost:
                continue
            heapq.heappush(frontier, (
                heuristic(n[0], n[1]) + next_cost, n, [state[1]] + state[2], next_cost, heuristic(n[0], n[1])))
            counter += 1

    if state[0] != dst:
        return path

    src = (3, 6)
dst = (15, 15)

path = astar(binaryMatrixBackUp)

if len(path) != 0:
    print("path2 is:")
    print(path, "\n")
    print("cost of shortest path2 is:\t", len(path))
    print("number of expanded node is:\t", counter)

    aStar_traversal2 = []
    for item in path:
        item = item[0] * 20 + item[1]
        aStar_traversal2.append(item)

printMatrixWithPath("A *", matrix, aStar_traversal1 + aStar_traversal2)
'''
