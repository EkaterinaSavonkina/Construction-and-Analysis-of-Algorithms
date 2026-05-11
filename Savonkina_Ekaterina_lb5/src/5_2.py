# Функция поиска шаблона с джокером в тексте
# text - текст для поиска
# pattern - шаблон с джокерами
# wildcard - символ джокера (заменяет любой один символ)
def find_pattern_with_wildcard(text, pattern, wildcard):
    # parts - список подстрок шаблона без джокеров
    # positions - позиции этих подстрок в исходном шаблоне
    # current_part - текущая накапливаемая подстрока
    # current_pos - позиция начала текущей подстроки в шаблоне
    parts = []
    positions = []
    current_part = []
    current_pos = 0

    # разбиваем шаблон на подстроки без джокеров
    for i, char in enumerate(pattern):
        if char == wildcard:  # встретили джокер
            if current_part:  # если накопили символы до джокера
                parts.append(''.join(current_part))  # сохраняем подстроку
                positions.append(current_pos)  # сохраняем её позицию в шаблоне
                current_part = []  # сбрасываем текущую подстроку
            current_pos = i + 1  # следующая подстрока начнется после джокера
        else:  # обычный символ
            current_part.append(char)  # добавляем символ в текущую подстроку

    # не забываем последнюю подстроку если она есть
    if current_part:
        parts.append(''.join(current_part))
        positions.append(current_pos)

    # если нет ни одной подстроки без джокеров (шаблон только из джокеров)
    if not parts:
        return []

    # автомат Ахо-Корасик внутри функции
    class AhoCorasick:
        def __init__(self):
            self.children = []  # переходы: children[узел][символ] = дочерний узел
            self.fail = []  # суффиксные ссылки
            self.output = []  # какие подстроки заканчиваются в узле
            self.terminal = []  # конечные ссылки (до ближайшего узла с образцом)
            self._init_node()  # создаем корень

        def _init_node(self):
            # создаем новый пустой узел
            self.children.append({})  # пустой словарь переходов
            self.fail.append(0)  # суффиксная ссылка на корень
            self.output.append([])  # список подстрок пуст
            self.terminal.append(-1)  # конечной ссылки нет
            return len(self.children) - 1  # возвращаем номер узла

        def add_pattern(self, pattern, pattern_index):
            # добавляем одну безмасочную подстроку в бор
            node = 0  # начинаем с корня
            for char in pattern:  # идем по каждому символу
                if char not in self.children[node]:  # нет перехода по символу
                    self.children[node][char] = self._init_node()  # создаем узел
                node = self.children[node][char]  # переходим по символу
            self.output[node].append(pattern_index)  # в конце запоминаем номер подстроки

        def build(self):
            # строим суффиксные и конечные ссылки обходом в ширину
            queue = []  # очередь для BFS
            head = 0  # указатель на голову очереди

            # все дети корня получают суффиксную ссылку на корень
            for char, child in self.children[0].items():
                self.fail[child] = 0
                queue.append(child)

            # обходим бор по уровням
            while head < len(queue):
                current = queue[head]  # берем узел из очереди
                head += 1  # сдвигаем указатель

                # обрабатываем всех детей текущего узла
                for char, child in self.children[current].items():
                    queue.append(child)  # добавляем ребенка в очередь
                    fail_state = self.fail[current]  # начинаем с суффикса родителя

                    # идем по суффиксным ссылкам пока не найдем переход по символу
                    while fail_state != 0 and char not in self.children[fail_state]:
                        fail_state = self.fail[fail_state]

                    # если нашли переход ставим суффиксную ссылку
                    if char in self.children[fail_state]:
                        self.fail[child] = self.children[fail_state][char]
                    else:
                        self.fail[child] = 0  # иначе в корень

                # строим конечную ссылку
                if self.output[current]:  # если в узле есть подстроки
                    self.terminal[current] = current  # ссылаемся на себя
                else:  # если подстрок нет
                    self.terminal[current] = self.terminal[self.fail[current]]  # наследуем от суффикса

        def search(self, text):
            # поиск всех вхождений безмасочных подстрок в тексте
            node = 0  # начинаем с корня
            # массив счетчиков: для каждой позиции текста считаем сколько подстрок совпало
            match_counts = [0] * len(text)

            for pos, char in enumerate(text):  # идем по тексту
                # если не можем перейти по символу идем по суффиксным ссылкам
                while node != 0 and char not in self.children[node]:
                    node = self.fail[node]

                # переходим по символу если можем
                if char in self.children[node]:
                    node = self.children[node][char]
                else:
                    node = 0  # иначе остаемся в корне

                # собираем все подстроки через конечные ссылки
                term = self.terminal[node]
                while term != -1:  # пока есть куда идти
                    for pattern_index in self.output[term]:  # все подстроки в этом узле
                        part_len = len(parts[pattern_index])  # длина подстроки
                        # вычисляем где бы начинался шаблон если эта подстрока часть его
                        start_pos = pos - part_len - positions[pattern_index] + 1

                        # проверяем что шаблон помещается в текст
                        if start_pos >= 0 and start_pos + len(pattern) <= len(text):
                            match_counts[start_pos] += 1  # увеличиваем счетчик для этой позиции

                            # если все подстроки совпали для этой начальной позиции
                            if match_counts[start_pos] == len(parts):
                                yield start_pos + 1  # нашли вхождение (позиция с 1)
                    term = self.terminal[self.fail[term]]  # идем по цепочке конечных ссылок

    # создаем автомат
    ac = AhoCorasick()

    # добавляем все безмасочные подстроки в автомат
    for i, part in enumerate(parts):
        ac.add_pattern(part, i)

    # строим суффиксные и конечные ссылки
    ac.build()

    # запускаем поиск и возвращаем список позиций
    return list(ac.search(text))


def main():
    # читаем входные данные
    text = input().strip()  # текст
    pattern = input().strip()  # шаблон с джокерами
    wildcard = input().strip()  # символ джокера

    # ищем все вхождения шаблона
    result = find_pattern_with_wildcard(text, pattern, wildcard)

    # выводим позиции вхождений (каждую с новой строки)
    for pos in result:
        print(pos)


if __name__ == "__main__":
    main()