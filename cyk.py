from collections import defaultdict

GRAMMAR_RULES = "./grammar/chowsky"
SENTENCES = "input.txt"

def read_lines(filename):
    all_lines = list()
    with open(filename, "r") as file:
        for line in file.readlines():
            all_lines.append(line.replace("\n", ""))
    return all_lines

class Rule:
    def __init__(self, line):
        self.left = line.split(" -> ")[0]
        self.right = line.split(" -> ")[1].split(" | ")

class Grammar:
    def __init__(self, lines):
        '''Constructor for grammar class. Initializes grammar rules.'''
        super(Grammar, self).__init__()
        self.lines = lines
        self.rules = defaultdict(lambda: [])

        for line in lines:
            if line == "\r" or line == '' or line[0] == '#':
                continue
            rule = Rule(line)
            self.rules[rule.left].append(rule.right)
            for i in self.rules[rule.left][0]:
                self.rules[rule.left].append(list(map(lambda x : x[1:-1] if ("'" in x) else x, i.split(" "))))
            self.rules[rule.left] = self.rules[rule.left][1:]

def search_rules(grammar, right):
    matches = []
    for left in grammar.rules:
        for rule in grammar.rules[left]:
            # print(rule)
            if rule == right:
                matches.append(left)
    return matches

def parse(sentence, grammar):
    print("=========================")
    print(sentence)
    print("=========================")
    
    words = [i for i in sentence]
    for i in range(len(words)):
        if words[i] == ' ':
            words[i] = '~'
        elif words[i] == '\t':
            words[i] = '$'
        elif words[i] == '\r':
            words[i] = ';'
        elif words[i] == '\n':
            words[i] = ''

    table = []  # Inits empty table.

    for x in range(len(sentence)):
        table.append([])
        for y in range(len(sentence)):
            table[x].append([])
    
    # Algoritma 1
    for column in range(len(words)):
        table[column][column] = search_rules(grammar, [words[column]])
        for row in reversed(range(column + 1)):
            for s in range(row + 1, column + 1):
                for non_terminal1 in table[row][s - 1]:
                    for non_terminal2 in table[s][column]:
                        non_term = [non_terminal1, non_terminal2]
                        table[row][column].extend(search_rules(grammar, non_term))

    for i in table[0][len(table)-1]:
        if i == 'S':
            print("Accepted")
            break

    return table


grammar = read_lines(GRAMMAR_RULES)
sentences = read_lines(SENTENCES)

grammar = Grammar(grammar)
# print(grammar)

for sentence in sentences:
    parse_table = parse(sentence, grammar)
    print()
    # Print Tabel
    for row in range(len(parse_table)):
        for col in range(len(parse_table)):
            print(parse_table[row][col], end="")
        print()
