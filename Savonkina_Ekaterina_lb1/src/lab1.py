def divisor(n):
    """Поиск наибольшего делителя"""
    for i in range(n // 2, 0, -1):
        if n % i == 0:
            return i
    return 1

def search_free_cell(field, SIZE):
    """Поиск свободной клетке (самой левой, самой верхней)"""
    for y in range(SIZE):
        for x in range(SIZE):
            if field[y][x] == 0:
                return x, y
    return None, None

def can_place(field, x, y, n, SIZE):
    """Проверка на заполненность"""
    if x + n > SIZE or y + n > SIZE:
        return False
    for i in range(y, y + n):
        for j in range(x, x + n):
            if field[i][j] != 0:
                return False
    return True

def place(field, x, y, n):
    """Установка квадрата"""
    for i in range(y, y + n):
        for j in range(x, x + n):
            field[i][j] = n

def delete(field, x, y, n):
    """Удаление квадрата"""
    for i in range(y, y + n):
        for j in range(x, x + n):
            field[i][j] = 0

def max_square(x, y, SIZE):
    """Выбор максимального размера"""
    return min(SIZE - x, SIZE - y, (SIZE + 1) // 2)

def recursion(field, SIZE, tmp_pos, tmp_cnt, best_cnt, best_pos):
    if tmp_cnt >= best_cnt[0]:
        print(f"Текущее количество квадратов {tmp_cnt} уже больше (или равно) одного из прошлых, останавливаемся\n")
        return

    x, y = search_free_cell(field, SIZE)
    if x is None:
        best_cnt[0] = tmp_cnt
        best_pos.clear()
        best_pos.extend(tmp_pos)
        print(f"Квадрат полностью заполнен, количество: {best_cnt[0]}\n")
        return
    print(f"Текущее место: {x, y}")

    max_size = max_square(x, y, SIZE)
    print(f"Максимальный размер квадарата на этой клетке: {max_size}")

    for n in range(max_size, 0, -1):
        if can_place(field, x, y, n, SIZE):
            print(f"Пробуем квадрат {n}")
            print("Место есть, ставим")
            place(field, x, y, n)
            tmp_pos.append((x + 1, y + 1, n))
            tmp_cnt += 1

            for i in field:
                print(" ".join(map(str, i)))
            print("\nЗапускаем рекурсию")

            recursion(field, SIZE, tmp_pos, tmp_cnt, best_cnt, best_pos)

            print(f"Удаляем последний квадрат {n} на месте {x + 1, y + 1}")
            tmp_cnt -= 1
            tmp_pos.pop()
            delete(field, x, y, n)

            print("Поле после удаления:")
            for i in field:
                print(" ".join(map(str, i)))

    print("Квадраты всех возможных размеров использованы")

def run_algorithm(n):
    gsd = divisor(n)
    SIZE = n // gsd

    field = [[0] * SIZE for _ in range(SIZE)]
    tmp_pos = []
    tmp_cnt = 0
    best_cnt = [float('inf')]
    best_pos = []

    print(f"Заданный размер {SIZE * gsd}, будем решать задачу для {SIZE}\n")

    if SIZE % 2 == 1:
        big_sq = (SIZE + 1) // 2
        small_sq = big_sq - 1

        print(f"Ставим 3 квадрата: один квадрат размера {big_sq} и два размера {small_sq}\n")

        place(field, 0, 0, big_sq)
        tmp_pos.append((1, 1, big_sq))

        place(field, big_sq, 0, small_sq)
        tmp_pos.append((big_sq + 1, 1, small_sq))

        place(field, 0, big_sq, small_sq)
        tmp_pos.append((1, big_sq + 1, small_sq))

        tmp_cnt = 3

        print("Расстановка начальных квадратов (для оптимизации):")
        for i in field:
            print(" ".join(map(str, i)))
        print()

    print("Запускаем рекурсию")
    recursion(field, SIZE, tmp_pos, tmp_cnt, best_cnt, best_pos)
    print("Рекурсия окончена")

    print(best_cnt[0])
    for x, y, w in best_pos:
        print((x - 1) * gsd + 1, (y - 1) * gsd + 1, w * gsd)

if __name__ == '__main__':
    run_algorithm(int(input()))