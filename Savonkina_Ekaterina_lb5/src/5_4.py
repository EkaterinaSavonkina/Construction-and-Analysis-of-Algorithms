def find_pattern_with_wildcard(text, pattern, wildcard):
    parts = []
    positions = []
    current_part = []
    current_pos = 0

    print(f"Шаблон: {pattern}, джокер: {wildcard}")

    for i, char in enumerate(pattern):
        if char == wildcard:
            if current_part:
                parts.append(''.join(current_part))
                positions.append(current_pos)
                print(f"Часть {len(parts)}: '{parts[-1]}', позиция в шаблоне {current_pos}")
                current_part = []
            current_pos = i + 1
        else:
            current_part.append(char)

    if current_part:
        parts.append(''.join(current_part))
        positions.append(current_pos)
        print(f"Часть {len(parts)}: '{parts[-1]}', позиция в шаблоне {current_pos}")

    if not parts:
        print("Нет безмасочных частей")
        return [], 0

    print(f"\nБезмасочные части: {parts}")
    print(f"Позиции частей в шаблоне: {positions}")
    print(f"Длина шаблона: {len(pattern)}")

    class AhoCorasick:
        def __init__(self):
            self.children = []
            self.fail = []
            self.output = []
            self.terminal = []
            self._init_node()

        def _init_node(self):
            self.children.append({})
            self.fail.append(0)
            self.output.append([])
            self.terminal.append(-1)
            node_id = len(self.children) - 1
            print(f"  Создан узел {node_id}")
            return node_id

        def add_pattern(self, pattern, pattern_index):
            print(f"\n  Добавление части {pattern_index + 1}: '{pattern}'")
            node = 0
            for char in pattern:
                print(f"    узел {node}, символ {char}")
                if char not in self.children[node]:
                    new_node = self._init_node()
                    self.children[node][char] = new_node
                    print(f"    новое ребро: {node} {char} {new_node}")
                else:
                    print(f"    ребро существует: {node} {char} {self.children[node][char]}")
                node = self.children[node][char]
            self.output[node].append(pattern_index)
            print(f"    часть {pattern_index + 1} заканчивается в узле {node}")
            print(f"    output[{node}] = {self.output[node]}")

        def get_vertex_count(self):
            return len(self.children)

        def build(self):
            print("\n  Построение fail и terminal ссылок")
            queue = []
            head = 0

            print("  Дети корня получают fail=0")
            for char, child in self.children[0].items():
                self.fail[child] = 0
                queue.append(child)
                print(f"    fail[{child}] = 0, в очередь добавлен {child}")

            print(f"  Очередь: {queue}")

            while head < len(queue):
                current = queue[head]
                head += 1
                print(f"\n  Обработка узла {current}")

                for char, child in self.children[current].items():
                    print(f"    ребро: {current} {char} {child}")
                    queue.append(child)
                    fail_state = self.fail[current]
                    print(f"    начало поиска fail из {fail_state}")

                    while fail_state != 0 and char not in self.children[fail_state]:
                        print(
                            f"      нет {char} в узле {fail_state}, переход по fail[{fail_state}] = {self.fail[fail_state]}")
                        fail_state = self.fail[fail_state]

                    if char in self.children[fail_state]:
                        self.fail[child] = self.children[fail_state][char]
                        print(f"    найден {char} в узле {fail_state}, fail[{child}] = {self.fail[child]}")
                    else:
                        self.fail[child] = 0
                        print(f"    не найден, fail[{child}] = 0")

                    print(f"    fail[{child}] = {self.fail[child]}")

                if self.output[current]:
                    self.terminal[current] = current
                    print(f"    terminal[{current}] = {current} (есть части {self.output[current]})")
                else:
                    self.terminal[current] = self.terminal[self.fail[current]]
                    print(
                        f"    terminal[{current}] = terminal[{self.fail[current]}] = {self.terminal[current]} (частей нет)")

            print("\n  Построенный автомат:")
            for i in range(len(self.children)):
                children_str = " ".join([f"{c}:{v}" for c, v in self.children[i].items()])
                if not children_str:
                    children_str = "нет"
                print(
                    f"    Узел {i}: ребра={{{children_str}}}, fail={self.fail[i]}, output={self.output[i]}, terminal={self.terminal[i]}")

        def search(self, text):
            print(f"\n  Поиск в тексте: '{text}'")
            print(f"  Длина текста: {len(text)}")
            node = 0
            match_counts = [0] * len(text)
            wildcard_matches = []

            for pos, char in enumerate(text):
                print(f"\n    Позиция {pos}, символ {char}:")
                print(f"      текущий узел: {node}")

                if char not in self.children[node]:
                    print(f"      прямого перехода по {char} из узла {node} нет")

                while node != 0 and char not in self.children[node]:
                    print(f"      переход по fail: {node} {self.fail[node]}")
                    node = self.fail[node]

                if char in self.children[node]:
                    old_node = node
                    node = self.children[node][char]
                    print(f"      переход: {old_node} {char} {node}")
                else:
                    print(f"      остаемся в корне (узел 0)")
                    node = 0

                print(f"      узел после перехода: {node}")
                print(f"      terminal[{node}] = {self.terminal[node]}")

                term = self.terminal[node]
                if term == -1:
                    print(f"      частей не найдено")

                while term != -1:
                    print(f"      обработка terminal-узла: {term}")
                    for pattern_index in self.output[term]:
                        part_len = len(parts[pattern_index])
                        start_pos = pos - part_len - positions[pattern_index] + 1
                        print(f"        часть {pattern_index + 1} ('{parts[pattern_index]}') найдена")
                        print(f"        часть в шаблоне на позиции {positions[pattern_index]}")
                        print(f"        предполагаемое начало шаблона: {start_pos}")

                        if start_pos >= 0 and start_pos + len(pattern) <= len(text):
                            match_counts[start_pos] += 1
                            print(f"        match_counts[{start_pos}] = {match_counts[start_pos]} (нужно {len(parts)})")

                            if match_counts[start_pos] == len(parts):
                                print(f"        ВСЕ ЧАСТИ НАЙДЕНЫ, шаблон начинается с позиции {start_pos + 1}")
                                wildcard_matches.append((start_pos, start_pos + len(pattern) - 1))
                        else:
                            if start_pos < 0:
                                print(f"        выход за левую границу текста")
                            else:
                                print(
                                    f"        выход за правую границу текста (шаблон длины {len(pattern)} не помещается с позиции {start_pos})")
                    term = self.terminal[self.fail[term]]
                    if term != -1:
                        print(f"      переход к следующему terminal: terminal[fail] = {term}")

            print(f"\n  Итоговый match_counts: {match_counts}")
            return wildcard_matches

    ac = AhoCorasick()

    for i, part in enumerate(parts):
        ac.add_pattern(part, i)

    ac.build()

    vertex_count = ac.get_vertex_count()
    wildcard_matches = ac.search(text)

    print(f"\nНайденные вхождения шаблона (интервалы в тексте):")
    for start, end in wildcard_matches:
        print(f"  [{start}, {end}] (позиция {start + 1})")

    return wildcard_matches, vertex_count


def find_overlapping(matches):
    print("\nПоиск пересечений вхождений шаблона:")
    overlapping_matches = set()

    for i in range(len(matches)):
        start1, end1 = matches[i]
        print(f"  вхождение {i + 1}: [{start1}, {end1}]")

        for j in range(i + 1, len(matches)):
            start2, end2 = matches[j]
            print(f"    проверка с вхождением {j + 1}: [{start2}, {end2}]")

            if start1 <= end2 and start2 <= end1:
                print(f"      пересечение: [{start1},{end1}] и [{start2},{end2}]")
                overlapping_matches.add(i)
                overlapping_matches.add(j)
            else:
                print(f"      пересечения нет")

    return overlapping_matches


def main():
    text = input().strip()
    pattern = input().strip()
    wildcard = input().strip()

    wildcard_matches, vertex_count = find_pattern_with_wildcard(text, pattern, wildcard)

    print(f"\nКоличество вершин в автомате: {vertex_count}")

    print("\nПозиции вхождений шаблона:")
    for start, end in wildcard_matches:
        print(start + 1)

    overlapping = find_overlapping(wildcard_matches)
    print("\nПересекающиеся вхождения:")
    if overlapping:
        print("Пересечение:", *[i + 1 for i in sorted(overlapping)])
    else:
        print("Пересечение: нет")


if __name__ == "__main__":
    main()