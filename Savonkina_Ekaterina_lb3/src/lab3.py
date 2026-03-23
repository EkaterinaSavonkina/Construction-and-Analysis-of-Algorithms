def ins_cost(a):
    if sp_ins == a:
        return sp_ins_cost
    return 1

def rep_cost(a, b):
    if sp_rep == a:
        return sp_rep_cost
    if a == b:
        return 0
    return 1

def levenshtein(a, b):
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for i in range(n + 1)]
    dp[0][0] = 0

    print("Матрица до заполнения:")

    print("   ", end=" ")
    for ch in b:
        print(ch, end=" ")
    print()

    for i in range(len(dp)):
        if i == 0:
            print(" ", end=" ")
        else:
            print(a[i - 1], end=" ")

        for j in range(len(dp[0])):
            print(dp[i][j], end=" ")
        print()

    for i in range(n + 1):
        dp[i][0] = i

    for j in range(1, m + 1):
        dp[0][j] = dp[0][j - 1] + ins_cost(b[j - 1])

    print("Матрица после заполнения начальных строк:")

    print("   ", end=" ")
    for ch in b:
        print(ch, end=" ")
    print()

    for i in range(len(dp)):
        if i == 0:
            print(" ", end=" ")
        else:
            print(a[i - 1], end=" ")

        for j in range(len(dp[0])):
            print(dp[i][j], end=" ")
        print()

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            print(f"Рассматриваем клетку: ({i}, {j})")
            print("Возможные операции и их итоговая стоимость:")

            delete_cost = dp[i - 1][j] + 1
            print(f"Удаление '{a[i - 1]}': {dp[i - 1][j]} + 1 = {delete_cost}")

            insert_cost = dp[i][j - 1] + ins_cost(b[j - 1])
            print(f"Вставка '{b[j - 1]}': {dp[i][j - 1]} + {ins_cost(b[j - 1])} = {insert_cost}")

            replace_cost = dp[i - 1][j - 1] + rep_cost(a[i - 1], b[j - 1])
            print(
                f"Замена '{a[i - 1]}' -> '{b[j - 1]}': {dp[i - 1][j - 1]} + {rep_cost(a[i - 1], b[j - 1])} = {replace_cost}")

            dp[i][j] = min(delete_cost, insert_cost, replace_cost)

            print(f"Выбрано минимальное значение: {dp[i][j]}")

    print("Матрица после заполнения:")

    print("   ", end=" ")
    for ch in b:
        print(ch, end=" ")
    print()

    for i in range(len(dp)):
        if i == 0:
            print(" ", end=" ")
        else:
            print(a[i - 1], end=" ")

        for j in range(len(dp[0])):
            print(dp[i][j], end=" ")
        print()

    return dp[n][m]

a = input()
b = input()

sp_ins = input("Особо добавляемый: ")
if sp_ins:
    sp_ins_cost = int(input("Цена: "))
else:
    sp_ins = None
    sp_ins_cost = 1

sp_rep = input("Особо заменяемый: ")
if sp_rep:
    sp_rep_cost = int(input("Цена: "))
else:
    sp_rep = None
    sp_rep_cost = 1

print(levenshtein(a, b))



