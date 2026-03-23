def prefix_function(P):
    print("Строим префикс функцию")
    n = len(P)
    pi = n * [0]
    j = 0

    for i in range(1, n):
        while j > 0 and P[i] != P[j]:
            j = pi[j - 1]

        if P[i] == P[j]:
            j += 1

        pi[i] = j
        print(f"Для pi[{i}] = {j}: "
              f"рассматриваем '{P[:i+1]}', "
              f"совпадающий префикс '{P[:j]}'")

    print(f"Функция: {pi}")
    return pi

def kmp(P, T):
    pi = prefix_function(P)

    res = []
    j = 0

    print(f"\nИщем образец '{P}' в тексте '{T}'")

    for i in range(len(T)):

        print(f"\nРассматриваем символ текста '{T[i]}' (позиция {i})")

        while j > 0 and T[i] != P[j]:
            print(f"Не совпадает с образцом: '{T[i]}' != '{P[j]}'")
            print(f"Смотрим префикс-функцию pi[{j-1}] = {pi[j-1]}")
            j = pi[j - 1]
            print(f"Переходим к позиции в образце j = {j}")

        if T[i] == P[j]:
            print(f"Совпало: '{T[i]}' == '{P[j]}'")
            j += 1
            print(f"Уже: {P[:j]}")

        if j == len(P):
            start = i - j + 1
            print(f"\nсовпадение с позиции {start} в тексте")
            res.append(start)

            print(f"Используем префикс-функцию pi[{j-1}] = {pi[j-1]} для продолжения поиска")
            j = pi[j - 1]

    print(f"\nИтоговые позиции: {res}")
    return res

if __name__ == '__main__':
    P = input()
    T = input()

    res = kmp(P, T)

    if res == []:
        print(-1)
    else:
        print(','.join(map(str, res)))