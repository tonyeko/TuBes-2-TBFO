from collections import defaultdict
import itertools
import re

GRAMMAR_RULES = "../data/chowsky"
SENTENCES = "../data/test.py"

def read_lines(filename):
    '''Reads lines.'''
    all_lines = list()
    with open(filename, "r") as file:
        for line in file.readlines():
            all_lines.append(line.replace("\n", ""))
    return all_lines

def init_table(words):
    '''Initilizes empty table.'''
    table = []
    for x in range(len(words)):
        table.append([])
        for y in range(len(words)):
            table[x].append([])
    return table

def print_table(sentence, table):
    '''Prints given table.'''
    print()
    for row in range(len(table)):
        for col in range(row, len(table)):
            print(table[row][col], end="")
        print()


class Rule:
    '''Rule class.'''
    def __init__(self, line):
        self.left = line.split(" -> ")[0]
        self.right = line.split(" -> ")[1].split(" | ")

class Grammar:
    '''Grammar class.'''

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
                self.rules[rule.left].append(i.split(" "))
            self.rules[rule.left] = self.rules[rule.left][1:]

    def __str__(self):
        '''To string method of grammar class. '''
        return_string = ""
        for elem in self.rules.keys():
            return_string += elem + " -> " + str(self.rules[elem]) + "\n"
        return return_string


def find_matches(grammar, word, right1, right2):
    '''Searches possible rules given word or non_terminal.'''
    matches = []

    def search_rules(right):
        '''Compares rules with given word or non_terminal '''
        for left in grammar.rules:
            for rule in grammar.rules[left]:
                for rule2 in rule:
                    if rule2 == (word or non_terminal):
                        matches.append(left)

    if word:
        search_rules(word)
    else:
        # print(right1); print(right2)
        for non_terminal in itertools.product(right1, right2):
            search_rules(non_terminal)

    return matches


def parse(sentence, grammar):
    '''Parses given sentences given grammar rules.'''
    words = sentence.split()
    print("=========================")
    print(words)
    print("=========================")
    table = init_table(words)  # Inits empty table.
    for column in range(len(words)):
        # print(words[column])
        '# Fill bottom values . Important: Matrix is transposed. So, it fills diagonally.'
        table[column][column] = find_matches(grammar, words[column], None, None)
        for row in reversed(range(column + 1)):
            for s in range(row + 1, column + 1):
                table[row][column].extend(find_matches(grammar, None, table[row][s - 1], table[s][column]))
    return table


print("Parsing...")
grammar = read_lines(GRAMMAR_RULES)
sentences = read_lines(SENTENCES)

grammar = Grammar(grammar)
print(grammar)

for sentence in sentences:
    parse_table = parse(sentence, grammar)
    print_table(sentence, parse_table)

print("\n\n\nParsed sentences in", SENTENCES, "successfully")
