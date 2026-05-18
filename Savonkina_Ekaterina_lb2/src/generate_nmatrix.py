import random


def generate_graph(n, symmetric):

    graph = [[0] * n for _ in range(n)]
    for i in range(n):

        for j in range(n):
            if i == j:
                graph[i][j] = 0
            else:
                if symmetric:
                    if j > i:
                        weight = random.randint(0, 50)

                        graph[i][j] = weight
                        graph[j][i] = weight
                else:
                    graph[i][j] = random.randint(0, 50)

    return graph

n = int(input("количество городов: "))

sym = input("Матрица симметричная (y/n): ").lower()

symmetric = (sym == "y")

graph = generate_graph(n, symmetric)

filename = "graph.txt"

with open(filename, "w") as file:

    file.write(f"{n}\n")
    for row in graph:
        line = " ".join(map(str, row))
        file.write(line + "\n")
