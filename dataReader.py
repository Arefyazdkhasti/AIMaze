'''
G = nx.from_numpy_matrix(np.array(shit))
nx.draw(G, with_labels=True)

graph = dict()

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

plt.show()
'''

'''
# tree making
v = [[] for i in range(100)]


def addEdge(x, y):
    v[x].append(y)
    v[y].append(x)


current_x = 0
current_y = 0
# all four possible neighbors for each node store in this list

for i in range(0, 20):
    for j in range(0, 20):
        neighbors = []
        if j - 1 >= 0:
            if matrix[i][j-1] != 'W':
                neighbors.append([i, j - 1])
        if j + 1 < 20:
            if matrix[i][j+1] != 'W':
                neighbors.append([i, j + 1])
        if i + 1 < 20:
            if matrix[i+1][j] != 'W':
                neighbors.append([i + 1, j])
        if i - 1 >= 0:
            if matrix[i-1][j] != 'W':
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
