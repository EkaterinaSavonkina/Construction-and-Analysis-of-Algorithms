class AhoCorasick:
    def __init__(self):
        self.children = []
        self.fail = []
        self.output = []
        self.terminal = []
        self.dictionary = []
        self._init_node()

    def _init_node(self):
        self.children.append({})
        self.fail.append(0)
        self.output.append([])
        self.terminal.append(-1)
        node_id = len(self.children) - 1
        print(f"Создан узел {node_id}")
        return node_id

    def add_pattern(self, pattern, pattern_index):
        print(f"\nДобавление образца {pattern_index + 1}: {pattern}")
        node = 0
        for char in pattern:
            print(f"  узел {node}, символ {char}")
            if char not in self.children[node]:
                new_node = self._init_node()
                self.children[node][char] = new_node
                print(f"  новое ребро: {node} {char} {new_node}")
            else:
                print(f"  ребро существует: {node} {char} {self.children[node][char]}")
            node = self.children[node][char]
        self.output[node].append(pattern_index)
        print(f"  образец {pattern_index + 1} заканчивается в узле {node}")
        print(f"  output[{node}] = {self.output[node]}")

    def build(self):
        print("\nПостроение fail и terminal ссылок")
        queue = []
        head = 0

        print("Дети корня получают fail=0")
        for char, child in self.children[0].items():
            self.fail[child] = 0
            queue.append(child)
            print(f"  fail[{child}] = 0, в очередь добавлен {child}")

        print(f"Очередь: {queue}")

        while head < len(queue):
            current = queue[head]
            head += 1
            print(f"\nОбработка узла {current}")

            for char, child in self.children[current].items():
                print(f"  ребро: {current} {char} {child}")
                queue.append(child)
                fail_state = self.fail[current]
                print(f"  начало поиска fail из {fail_state}")

                while fail_state != 0 and char not in self.children[fail_state]:
                    print(
                        f"    нет {char} в узле {fail_state}, переход по fail[{fail_state}] = {self.fail[fail_state]}")
                    fail_state = self.fail[fail_state]

                if char in self.children[fail_state]:
                    self.fail[child] = self.children[fail_state][char]
                    print(f"  найден {char} в узле {fail_state}, fail[{child}] = {self.fail[child]}")
                else:
                    self.fail[child] = 0
                    print(f"  не найден, fail[{child}] = 0")

                print(f"  fail[{child}] = {self.fail[child]}")

            if self.output[current]:
                self.terminal[current] = current
                print(f"  terminal[{current}] = {current} (есть образцы {self.output[current]})")
            else:
                self.terminal[current] = self.terminal[self.fail[current]]
                print(
                    f"  terminal[{current}] = terminal[{self.fail[current]}] = {self.terminal[current]} (образцов нет)")

        print("\nПостроенный автомат:")
        for i in range(len(self.children)):
            children_str = " ".join([f"{c}:{v}" for c, v in self.children[i].items()])
            if not children_str:
                children_str = "нет"
            print(
                f"  Узел {i}: ребра={{{children_str}}}, fail={self.fail[i]}, output={self.output[i]}, terminal={self.terminal[i]}")

    def get_vertex_count(self):
        return len(self.children)

    def search(self, text):
        print(f"\nПоиск в тексте: {text}")
        results = []
        node = 0

        for pos, char in enumerate(text):
            print(f"\n  Позиция {pos}, символ {char}:")
            print(f"    текущий узел: {node}")

            if char not in self.children[node]:
                print(f"    прямого перехода по {char} из узла {node} нет")

            while node != 0 and char not in self.children[node]:
                print(f"    переход по fail: {node} {self.fail[node]}")
                node = self.fail[node]

            if char in self.children[node]:
                old_node = node
                node = self.children[node][char]
                print(f"    переход: {old_node} {char} {node}")
            else:
                print(f"    остаемся в корне (узел 0)")
                node = 0

            print(f"    узел после перехода: {node}")
            print(f"    terminal[{node}] = {self.terminal[node]}")

            term = self.terminal[node]
            if term == -1:
                print(f"    образцов не найдено")

            while term != -1:
                print(f"    обработка terminal-узла: {term}")
                for pattern_index in self.output[term]:
                    pattern_len = len(self.dictionary[pattern_index])
                    start_pos = pos - pattern_len + 1
                    print(f"      найден образец {pattern_index + 1} ({self.dictionary[pattern_index]})")
                    print(f"      длина={pattern_len}, начало={start_pos + 1}")
                    results.append((start_pos + 1, pattern_index + 1))
                term = self.terminal[self.fail[term]]
                if term != -1:
                    print(f"    переход к следующему terminal: terminal[fail] = {term}")

        return results

    def find_overlapping(self, results):
        print("\nПоиск пересечений:")
        overlapping_patterns = set()

        for i in range(len(results)):
            pos1, pat1 = results[i]
            end1 = pos1 + len(self.dictionary[pat1 - 1]) - 1
            print(f"  вхождение {i}: образец {pat1} ({self.dictionary[pat1 - 1]}), позиции [{pos1}, {end1}]")

            for j in range(i + 1, len(results)):
                pos2, pat2 = results[j]
                end2 = pos2 + len(self.dictionary[pat2 - 1]) - 1
                print(
                    f"    проверка с вхождением {j}: образец {pat2} ({self.dictionary[pat2 - 1]}), позиции [{pos2}, {end2}]")

                if pos1 <= end2 and pos2 <= end1:
                    print(f"      пересечение найдено: [{pos1},{end1}] и [{pos2},{end2}]")
                    overlapping_patterns.add(pat1)
                    overlapping_patterns.add(pat2)
                else:
                    print(f"      пересечения нет")

        return sorted(overlapping_patterns)


def main():
    text = input().strip()
    n = int(input())

    ac = AhoCorasick()

    for i in range(n):
        pattern = input().strip()
        ac.dictionary.append(pattern)
        ac.add_pattern(pattern, i)

    ac.build()

    vertex_count = ac.get_vertex_count()
    print(f"\nКоличество вершин: {vertex_count}")

    results = ac.search(text)
    results.sort(key=lambda x: (x[0], x[1]))

    print("\nРезультаты поиска:")
    for pos, pat_num in results:
        print(f"{pos} {pat_num}")

    overlapping = ac.find_overlapping(results)
    print("\nПересекающиеся образцы:")
    if overlapping:
        print("Пересечение:", *overlapping)
    else:
        print("Пересечение: нет")


if __name__ == "__main__":
    main()