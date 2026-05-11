class AhoCorasick:
    def __init__(self):
        # тут хранятся все узлы и их данные
        self.children = []  # в детей пишем словари: символ -> номер узла
        self.fail = []  # суффиксные ссылки
        self.output = []  # какие образцы заканчиваются в этом узле
        self.terminal = []  # сжатые ссылки до ближайшего образца
        self.dictionary = []  # оригинальные строки образцов
        self._init_node()  # создаем корень

    def _init_node(self):
        # создаем новый пустой узел
        self.children.append({})  # пустой словарь переходов
        self.fail.append(0)  # суффиксная ссылка пока на корень
        self.output.append([])  # список образцов пустой
        self.terminal.append(-1)  # минус один значит нет образца
        return len(self.children) - 1  # номер созданного узла

    def add_pattern(self, pattern, pattern_index):
        # добавляем один образец в бор
        node = 0  # начинаем с корня
        for char in pattern:  # идем по каждому символу
            if char not in self.children[node]:  # если нет перехода
                self.children[node][char] = self._init_node()  # создаем новый узел
            node = self.children[node][char]  # переходим по символу
        self.output[node].append(pattern_index)  # в конце запоминаем номер образца

    def build(self):
        # строим суффиксные и конечные ссылки обходом в ширину
        queue = []  # очередь для обхода
        head = 0  # указатель на голову очереди

        # все дети корня получают суффиксную ссылку на корень
        for char, child in self.children[0].items():
            self.fail[child] = 0
            queue.append(child)

        # обходим все узлы
        while head < len(queue):
            current = queue[head]
            head += 1

            # обрабатываем всех детей текущего узла
            for char, child in self.children[current].items():
                queue.append(child)  # добавляем ребенка в очередь
                fail_state = self.fail[current]  # начинаем поиск с суффикса родителя

                # идем по цепочке fail пока не найдем переход по нужному символу
                while fail_state != 0 and char not in self.children[fail_state]:
                    fail_state = self.fail[fail_state]

                # если нашли переход ставим ссылку туда
                if char in self.children[fail_state]:
                    self.fail[child] = self.children[fail_state][char]
                else:
                    self.fail[child] = 0  # иначе ссылаемся на корень

            # строим конечную ссылку
            if self.output[current]:  # если в узле есть образцы
                self.terminal[current] = current  # ссылаемся сам на себя
            else:  # если образцов нет
                self.terminal[current] = self.terminal[self.fail[current]]  # берем от суффикса

    def search(self, text):
        # ищем все образцы в тексте
        results = []  # сюда будем сохранять найденные вхождения
        node = 0  # начинаем с корня

        for pos, char in enumerate(text):  # идем по тексту
            # если не можем перейти по символу идем по суффиксным ссылкам
            while node != 0 and char not in self.children[node]:
                node = self.fail[node]

            # переходим по символу если можем
            if char in self.children[node]:
                node = self.children[node][char]
            else:
                node = 0  # иначе сидим в корне

            # собираем все образцы через конечные ссылки
            term = self.terminal[node]
            while term != -1:  # пока есть куда идти
                for pattern_index in self.output[term]:  # все образцы в этом узле
                    pattern_len = len(self.dictionary[pattern_index])  # длина образца
                    start_pos = pos - pattern_len + 1  # вычисляем начало
                    results.append((start_pos + 1, pattern_index + 1))  # добавляем с единиц
                term = self.terminal[self.fail[term]]  # идем дальше по цепочке

        return results


def main():
    text = input().strip()  # текст
    n = int(input())  # количество образцов

    ac = AhoCorasick()  # создаем автомат

    # добавляем все образцы
    for i in range(n):
        pattern = input().strip()  # читаем образец
        ac.dictionary.append(pattern)  # сохраняем строку
        ac.add_pattern(pattern, i)  # добавляем в автомат

    ac.build()  # строим ссылки

    results = ac.search(text)  # ищем
    results.sort(key=lambda x: (x[0], x[1]))  # сортируем по позиции потом по номеру

    # выводим
    for pos, pat_num in results:
        print(pos, pat_num)


if __name__ == "__main__":
    main()