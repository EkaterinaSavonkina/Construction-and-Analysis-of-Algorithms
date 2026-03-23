def prefix_function(P):
    n = len(P)
    pi = [0] * n
    j = 0

    print("Строим префикс функцию")

    for i in range(1, n):
        while j > 0 and P[i] != P[j]:
            j = pi[j - 1]

        if P[i] == P[j]:
            j += 1

        pi[i] = j
        print(f"Для pi[{i}] = {j}: рассматриваем '{P[:i+1]}', совпадающий префикс '{P[:j]}'")

    print(f"Функция: {pi}")
    return pi


def kmp_cyclic(A, B):
    n = len(A)
    pi = prefix_function(A)
    j = 0

    print(f"\nИщем циклический сдвиг '{A}' в '{B*2}'")

    for i in range(2 * n):

        c = B[i % n]

        print(f"\nРассматриваем символ текста '{c}' (позиция {i % n} в B, шаг {i})")

        while j > 0 and c != A[j]:
            print(f"Не совпадает с образцом: '{c}' != '{A[j]}'")
            print(f"Смотрим префикс-функцию pi[{j-1}] = {pi[j-1]}")
            j = pi[j - 1]
            print(f"Переходим к позиции в образце j = {j}")

        if c == A[j]:
            print(f"Совпало: '{c}' == '{A[j]}'")
            j += 1
            print(f"Уже: {A[:j]}")

        if j == n:
            pos = i - n + 1
            print(f"\nсовпадение с позиции {pos} в удвоенной строке")

            if pos < n:
                shift = (n - pos) % n
                print(f"циклический сдвиг = {shift}")
                return shift
            else:
                print("совпадение вне допустимого диапазона")
                return -1

    print("\nсовпадение не найдено")
    return -1


if __name__ == '__main__':
    A = input().strip()
    B = input().strip()

    if len(A) != len(B):
        print(-1)
    else:
        print(kmp_cyclic(A, B))