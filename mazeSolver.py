from Astar import AStar
from UniformCostSearch import UniformCostSearch
from IterativeDeepeningSearch import IterativeDeepeningSearch
from queue import Queue
from termcolor import colored

filePath = "generated_maze.txt"

with open(filePath, "r") as file:
    matrix = [
        [x for x in line.split()]
        for line in file
    ]

for row in matrix:
    print(row)

# region figure binary matrix
binaryMatrix0 = [[0 for x in range(20)] for y in range(20)]
binaryMatrix0_pashmam = [[0 for x in range(20)] for y in range(20)]
matrix_with_holes_as_wall = [[0 for x in range(20)] for y in range(20)]
# for 3 new isPath i had to use this method
matrix_with_holes_as_wall_with_one = [[0 for x in range(20)] for y in range(20)]
matrix_with_holes_as_path = [[0 for x in range(20)] for y in range(20)]

for row in range(0, 20):
    for col in range(0, 20):
        if matrix[row][col] == '-' or matrix[row][col] == 'F' or matrix[row][col] == 'A' or matrix[row][col] == 'H':
            binaryMatrix0[row][col] = 0
            binaryMatrix0_pashmam[row][col] = 0
            matrix_with_holes_as_path[row][col] = 0
        elif matrix[row][col] == 'W':
            binaryMatrix0[row][col] = 1
            binaryMatrix0_pashmam[row][col] = 1
            matrix_with_holes_as_path[row][col] = -1

        if matrix[row][col] == '-' or matrix[row][col] == 'F' or matrix[row][col] == 'A':
            matrix_with_holes_as_wall[row][col] = 0
            matrix_with_holes_as_wall_with_one[row][col] = 0
        elif matrix[row][col] == 'W' or matrix[row][col] == 'H':
            matrix_with_holes_as_wall[row][col] = -1
            matrix_with_holes_as_wall_with_one[row][col] = 1


# endregion

def isPath(_arr, start_row, start_col, dst_row, dst_col):
    # directions
    Dir = [[0, 1], [0, -1], [1, 0], [-1, 0]]

    # queue
    q = [(start_row, start_col)]

    # until queue is empty
    while len(q) > 0:
        p = q[0]
        q.pop(0)

        # mark as visited
        _arr[p[0]][p[1]] = -1

        # destination is reached.
        if p == (dst_row - 1, dst_col - 1):
            return True

        # check all four directions
        for i in range(4):

            # using the direction array
            a = p[0] + Dir[i][0]
            b = p[1] + Dir[i][1]

            if (0 > a or a >= dst_row) or (0 > b or b >= dst_col) or _arr[a][b] == -1:
                continue
            # not blocked and valid
            q.append((a, b))
    return False


# region figure isPath
holeLessPathForFirstDst = True
holeLessPathForSecondDst = True

isPathFromStartToF1WithoutHoles = isPath(matrix_with_holes_as_wall, 0, 0, 4, 7)
isPathFromF1ToF2WithoutHoles = isPath(matrix_with_holes_as_wall, 4, 7, 16, 16)

isPathFromStartToF1WithHoles = isPath(matrix_with_holes_as_path, 0, 0, 4, 7)
isPathFromF1ToF2WithHoles = isPath(matrix_with_holes_as_path, 4, 7, 16, 16)

# TODO deal with these different occasions
if isPathFromStartToF1WithoutHoles:
    if isPathFromF1ToF2WithoutHoles:
        print("There are path from start to F1 and from F1 to F2 (holes consider as a wall)")
        holeLessPathForFirstDst = True
        holeLessPathForSecondDst = True
    else:
        print("There is path from start to F1 (holes consider as a wall)")
        holeLessPathForFirstDst = True
        holeLessPathForSecondDst = False
        if isPathFromF1ToF2WithHoles:
            print(
                "There is path from F1 to F2 (holes consider as a path) - you have to pass some holes to arrive at F2")
        else:
            print("There is no path available form F1 to F2")
else:
    if isPathFromF1ToF2WithoutHoles:
        print("There is a hole-less path from F1 to F2 but no hole-less path from start to F1")
        holeLessPathForFirstDst = False
        holeLessPathForSecondDst = True
    else:
        print("There are no hole-less path at all")
        holeLessPathForFirstDst = False
        holeLessPathForSecondDst = False
        if isPathFromStartToF1WithHoles:
            print("F1 to F2 has a hole-less path but start to end doesn't")
        else:
            print("There is no path available at all")

print(holeLessPathForFirstDst, holeLessPathForSecondDst)

# if hole less path exists do not pass the holes

if holeLessPathForFirstDst:
    for row in range(0, 4):
        for col in range(0, 7):
            if matrix[row][col] == 'H':
                binaryMatrix0[row][col] = 1
                binaryMatrix0_pashmam[row][col] = 1
            # binaryMatrix1[row][col] = 0
else:
    if isPath(matrix_with_holes_as_wall_with_one, 0, 0, 6, 7) or isPath(matrix_with_holes_as_wall_with_one, 0, 0, 5, 7) or isPath(
            matrix_with_holes_as_wall_with_one, 0, 0, 4, 8):
        for row in range(0, 4):
            for col in range(0, 7):
                if matrix[row][col] == 'H':
                    binaryMatrix0[row][col] = 1
                    binaryMatrix0_pashmam[row][col] = 1

if holeLessPathForSecondDst:
    for row in range(3, 16):
        for col in range(7, 16):
            if matrix[row][col] == 'H':
                binaryMatrix0[row][col] = 1
                binaryMatrix0_pashmam[row][col] = 1
else:
    if isPath(matrix_with_holes_as_wall_with_one, 0, 0, 17, 16) or isPath(matrix_with_holes_as_wall_with_one, 0, 0, 18, 16) or isPath(
            matrix_with_holes_as_wall_with_one, 0, 0, 16, 17):
        for row in range(3, 16):
            for col in range(7, 16):
                if matrix[row][col] == 'H':
                    binaryMatrix0[row][col] = 1


# endregion

# region figure adjacency list
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


# endregion

matrix_IDDFS = matrix
matrix_AStar = matrix
matrix_USF = matrix

def printMatrixWithPath(algorithm_name, _matrix, _path, expandedNodes=0):
    print("*************" ,_path)
    print(colored("------------------------- Algorithm: " + algorithm_name + "------------------------", 'green'))

    for row in range(0, len(_matrix)):
        for col in range(0, len(_matrix)):
            if 20 * row + col in _path:
                if _matrix[row][col] == 'H' or _matrix[row][col] == 'J':
                    print(colored("you pass over holes is " + str(row) + " " + str(col), 'magenta'))
                    _matrix[row][col] = "J"  # holes that you have to pass!
                else:
                    _matrix[row][col] = "*"

    for row in range(0, len(_matrix)):
        for col in range(0, len(_matrix)):
            if _matrix[row][col] == "*":
                print(colored(" * ", 'blue'), end=" ")
            elif _matrix[row][col] == "W":
                print(colored(" W ", 'red'), end=" ")
            elif _matrix[row][col] == "J":
                print(colored(" J ", 'yellow'), end=" ")
            elif _matrix[row][col] == "H":
                print(" H ", end=" ")
            else:
                print(" " + _matrix[row][col] + " ", end=" ")
        print()

    print("Shortest Path is: ", _path)
    print("Cost of the Shortest path is: ", len(_path))
    if expandedNodes != 0:
        print("Expand Node Numbers: ", expandedNodes)
    _path.clear()



# todo path for IDDFS is wrong!!! - hole BFS return wrong due to wrong adjacency list which not updated with holes


# region A*
src1 = (0, 0)
dst1 = (3, 6)
aStar = AStar(binaryMatrix0)
path1_AStar = aStar.aStar(src1, dst1)

if len(path1_AStar) != 0:

    aStar_traversal1 = []
    for item in path1_AStar:
        item = item[0] * 20 + item[1]
        aStar_traversal1.append(item)
else:
    print("shortest path doesn't exist")

src2 = (3, 6)
dst2 = (15, 15)
aStar = AStar(binaryMatrix0)
path2_AStar = aStar.aStar(src2, dst2)

if len(path2_AStar) != 0:

    aStar_traversal2 = []
    for item in path2_AStar:
        item = item[0] * 20 + item[1]
        aStar_traversal2.append(item)
else:
    print("shortest path doesn't exist")

final_path = list(aStar_traversal1 + aStar_traversal2)
# 66 appear twice in the list one for dst of path1 and two for src of path2
final_path.remove(66)
printMatrixWithPath("A *", matrix_AStar, final_path)

# endregion

# region UCS
ucs = UniformCostSearch(binaryMatrix0)
path1_ucs = ucs.ucsShortestPath((0, 0), (3, 6))
path2_ucs = ucs.ucsShortestPath((3, 6), (15, 15))
total_cost = path1_ucs[0] + path2_ucs[0]
final_path = list(path1_ucs[1] + path2_ucs[1])
# (3,6) appeared twice
final_path.remove((3, 6))
# print(final_path)

traversal_ucs = []
for item in final_path:
    item = item[0] * 20 + item[1]
    traversal_ucs.append(item)

# print(traversal)
printMatrixWithPath("Uniform Cost Search", matrix_USF, traversal_ucs)
# endregion

# region IDDFS

ids1 = IterativeDeepeningSearch(binaryMatrix0_pashmam, (0, 0), (3, 6))
numberOfVisitedNodes, IterativeParent, IterativeCounter = ids1.iterative_search(400)
path_list1_iddfs = ids1.getPath()

ids2 = IterativeDeepeningSearch(binaryMatrix0_pashmam, (3, 6), (15, 15))
numberOfVisitedNodes2, IterativeParent2, IterativeCounter2 = ids2.iterative_search(400)
path_list2_iddfs = ids2.getPath()

path_IDDFS = path_list1_iddfs + path_list2_iddfs
path_IDDFS.remove((3, 6))

final_path_IDDFS = []

for item in path_IDDFS:
    final_path_IDDFS.append(item[0] * 20 + item[1])

printMatrixWithPath("Iterative Deepening Search", matrix_IDDFS, final_path_IDDFS)

# endregion

'''
# region BFS
def BFS(adj_list, start_node, target_node):
    # Set of visited nodes to prevent loops
    visited = set()
    queue = Queue()

    # queue for all items that put in the main queue without pop anything
    bfs_queue = Queue()
    # numbers of expanded nodes
    length = 0

    # Add the start_node to the queue and visited list
    queue.put(start_node)
    bfs_queue.put(start_node)
    visited.add(start_node)

    # start_node has not parents
    parent = dict()
    parent[start_node] = None

    # Perform step 3
    path_found = False
    while not queue.empty():
        current_node = queue.get()
        if current_node == target_node:
            path_found = True
            break

        for next_node in adj_list[current_node]:
            if next_node not in visited:
                queue.put(next_node)
                bfs_queue.put(next_node)
                parent[next_node] = current_node
                visited.add(next_node)

    length = len(bfs_queue.queue) - len(queue.queue)

    # Path reconstruction
    path = []
    if path_found:
        path.append(target_node)
        while parent[target_node] is not None:
            path.append(parent[target_node])
            target_node = parent[target_node]
        path.reverse()
    return path, length


path_bfs1, len1 = BFS(graph, 0, 66)
path_bfs2, len2 = BFS(graph, 66, 315)
final_path_bfs = path_bfs1 + path_bfs2
final_path_bfs.remove(66)

matrix_BFS = matrix
printMatrixWithPath("BFS", matrix_BFS, final_path_bfs, len1 + len2)
# endregion
'''

'''
binaryMatrixBackUp = binaryMatrix0


def bfs(visit_complete, graph, current_node, target_node):
    visit_complete.append(current_node)
    queue = []
    pth = []
    queue.append(current_node)

    while queue:
        s = queue.pop(0)
        print(s, end=" ")
        pth.append(s)
        if s == target_node:
            break

        for neighbour in graph[s]:
            if neighbour not in visit_complete:
                visit_complete.append(neighbour)
                queue.append(neighbour)
    return pth


pth = bfs([], graph, 0, 66)
printMatrixWithPath("SGHIT", matrix, pth)


def depth_first_search(_graph, start, end):
    stack = [start]
    visited = set()
    while stack:
        vertex = stack.pop()
        if vertex in visited:
            continue
        yield vertex
        visited.add(vertex)
        if vertex == end:
            break
        for neighbor in _graph[vertex]:
            stack.append(neighbor)
    return visited


shit1 = list(depth_first_search(graph, 0, 66))
matrix_DFS1 = matrix
printMatrixWithPath("DFS 0 till 66", matrix_DFS1, shit1)
'''
