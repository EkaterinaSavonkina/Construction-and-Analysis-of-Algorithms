INF = float('inf')

print("Выберите способ ввода матрицы:")
print("1 - Ввести вручную")
print("2 - Считать из файла")

choice = input("Ваш выбор: ")

if choice == "1":
    n = int(input("Введите количество городов: "))
    print("Введите матрицу расстояний:")
    graph = [list(map(int, input().split())) for i in range(n)]


elif choice == "2":
    filename = input("Введите имя файла: ")
    with open(filename, "r") as file:
        lines = file.readlines()
    n = int(lines[0])
    graph = []
    for i in range(1, n + 1):
        row = list(map(int, lines[i].split()))
        graph.append(row)
else:
    print("Неверный выбор")
    exit()
memo = {}
parent = {}


def mask_to_binary(mask):
    return format(mask, f'0{n}b')


def tsp(mask, pos):

    print(f"Вызов tsp(mask={mask_to_binary(mask)}, pos={pos})")

    if mask == (1 << n) - 1:

        print("Все города посещены")

        if graph[pos][0] == 0:
            print(f"Из города {pos} нельзя вернуться в 0")
            return INF

        print(f"Возвращаемся из {pos} в 0")
        print(f"Стоимость возврата = {graph[pos][0]}")

        return graph[pos][0]

    if (mask, pos) in memo:

        print("Состояние уже вычислено")
        print(f"memo[{mask_to_binary(mask)}, {pos}] = {memo[(mask, pos)]}")

        return memo[(mask, pos)]

    best = INF
    best_city = -1

    print(f"Текущий город: {pos}")
    print(f"Текущая маска: {mask_to_binary(mask)}")

    for city in range(n):

        print(f"\nПробуем перейти в город {city}")

        if mask & (1 << city):
            print(f"Город {city} уже посещён")
            continue

        if graph[pos][city] == 0:
            print(f"Дороги из {pos} в {city} нет")
            continue

        print(f"Дорога существует: {pos} - {city}")
        print(f"Стоимость дороги = {graph[pos][city]}")

        new_mask = mask | (1 << city)

        print(f"Новая маска: {mask_to_binary(new_mask)}")

        recursive_cost = tsp(new_mask, city)

        if recursive_cost == INF:
            print(f"Путь через город {city} невозможен")
            continue

        total_cost = graph[pos][city] + recursive_cost

        print(f"Общая стоимость через {city} = "
              f"{graph[pos][city]} + {recursive_cost} = {total_cost}")

        if total_cost < best:

            print(f"Найден новый лучший маршрут через {city}")

            best = total_cost
            best_city = city

    memo[(mask, pos)] = best
    parent[(mask, pos)] = best_city

    print("\nИтог состояния")
    print(f"mask = {mask_to_binary(mask)}")
    print(f"pos = {pos}")
    print(f"best = {best}")
    print(f"best_city = {best_city}")

    return best


def nearest_neighbor(graph, n):

    print("АЛШ-1")

    visited = [False] * n

    path = [0]
    visited[0] = True

    current = 0
    total_cost = 0

    print(f"\nСтартуем из города 0")

    for step in range(n - 1):

        print(f"Шаг {step + 1}")

        best_city = -1
        best_dist = INF

        print(f"Текущий город: {current}")

        for city in range(n):

            print(f"\nПроверяем город {city}")

            if visited[city]:
                print(f"Город {city} уже посещён")
                continue

            if graph[current][city] == 0:
                print(f"Нет дороги из {current} в {city}")
                continue

            print(f"Есть дорога {current} - {city}")
            print(f"Стоимость = {graph[current][city]}")

            if graph[current][city] < best_dist:

                print(f"Город {city} - новый лучший сосед")

                best_dist = graph[current][city]
                best_city = city

        if best_city == -1:

            print("Не удалось найти следующий город")
            print("Маршрут невозможен")

            return None, None

        print(f"\nВыбираем город {best_city}")
        print(f"Стоимость перехода = {best_dist}")

        visited[best_city] = True

        path.append(best_city)

        total_cost += best_dist

        print(f"Текущая стоимость маршрута = {total_cost}")
        print(f"Текущий путь: {' - '.join(map(str, path))}")

        current = best_city

    print("Все города посещены")

    if graph[current][0] == 0:

        print(f"Из города {current} нельзя вернуться в 0")
        print("Цикл невозможен")

        return None, None

    print(f"Возвращаемся из {current} в 0")
    print(f"Стоимость возврата = {graph[current][0]}")

    total_cost += graph[current][0]

    path.append(0)

    print(f"\nИтоговая стоимость = {total_cost}")
    print(f"Итоговый путь: {' -'.join(map(str, path))}")

    return total_cost, path


print("Точный метод")

exact_cost = tsp(1, 0)

print("Ответ точного метода")

if exact_cost == INF:

    print("no path")

else:

    print(f"Минимальная стоимость = {exact_cost}")

    exact_path = [0]

    mask = 1
    pos = 0

    print("\nВосстановление пути:")

    while mask != (1 << n) - 1:

        next_city = parent[(mask, pos)]

        print(f"{pos} - {next_city}")

        exact_path.append(next_city)

        mask = mask | (1 << next_city)
        pos = next_city

    exact_path.append(0)

    print(f"{pos} - 0")

    print("\nОптимальный путь:")
    print(*exact_path)

approx_cost, approx_path = nearest_neighbor(graph, n)

print("Результат алш-1")

if approx_cost is None:

    print("no path")

else:

    print(f"Приближённая стоимость = {approx_cost}")

    print("Приближённый путь:")
    print(*approx_path)