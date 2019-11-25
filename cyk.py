from collections import defaultdict
import re

GRAMMAR_RULES = "./grammar/chowsky"
SENTENCES = "input.txt"

def read_grammar(filename):
    all_lines = list()
    with open(filename, "r") as file:
        for line in file.readlines():
            all_lines.append(line.replace("\n", ""))
    return all_lines

def read_python_file(filename):
    all_lines = list()
    with open(filename, "r") as file:
        for line in file.readlines():
            all_lines.append(line.replace("\n", ";").replace("\t", "$"))
    return all_lines

class Rule:
    def __init__(self, line):
        self.left = line.split(" -> ")[0]
        self.right = line.split(" -> ")[1].split(" | ")

class Grammar:
    def __init__(self, lines):
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
    #print("=========================")
    print(sentence)
    #print("=========================")
    words = [i for i in sentence]
    parts = re.split('\s|(?<!\d)[,.](?!\d)', sentence)
    word = sentence.split()     # Hilangin spasi
    word2 = re.split('[-+*/]', ''.join(word)) # hilangin simbol operator
    # word = sentence.split()
    for i in range(len(word)):
        for j in range(len(word2)):
            if word[i] == word2[j]:
                word[i] = 'x'
    words = ''.join(word)
    print(words)
    # words = [i for i in sentence]
    for i in range(len(words)):
        print(words[i])
        #print(words[i], end=" ")
        if words[i] == ' ':
            words[i] = '~'          # Kalau dimasukkin ke line.replace ngeprintnya jadi jelek
        if words[i] == '#':
            break
        #print(words[i])
        # if i < len(words)-1:
        #     if words[i]+words[i+1] == '\t':
        #         words[i:i+2] = '$'
        #     elif words[i]+words[i+1] == '\r':
        #         words[i:i+2] = ';'
        #     elif words[i]+words[i+1] == '\n':
        #         words[i:i+2] = ';'

    # table = [ [ [] for i in range(len(sentence)) ] for j in range(len(sentence)) ] 
    
    table = [ [ [] for i in range(len(words)) ] for j in range(len(words)) ] 

    # Algoritma 1
    for column in range(len(words)):
        # print(words[column])
        table[column][column] = search_rules(grammar, [words[column]])
        #print(table[column][column])
        for row in reversed(range(column + 1)):
            for s in range(row + 1, column + 1):
                for non_terminal1 in table[row][s - 1]:
                    for non_terminal2 in table[s][column]:
                        non_term = [non_terminal1, non_terminal2]
                        table[row][column].extend(search_rules(grammar, non_term))

    for i in table[0][len(table)-1]:
        if state[0] in i:
            state.pop(0)
            state.append('Accepted2')
            break
        elif i == 'S':
            state.pop(0)
            state.append('Accepted')
            break

    return table


grammar = read_grammar(GRAMMAR_RULES)
sentences = read_python_file(SENTENCES)
realtext = list(map(lambda x: x.replace('\n',''), open(SENTENCES, "r").readlines()))
grammar = Grammar(grammar)
# print(grammar)
print(sentences)
state = ['XXX']
error = 0
for i in range(len(sentences)):
    parse_table = parse(sentences[i], grammar)
    # Print Tabel

    for row in range(len(parse_table)):
        for col in range(len(parse_table)):
            print(parse_table[row][col], end="")
        print()

    print(realtext[i],end="    ")
    if not([] == list(filter(None,map(lambda x: x if ('Head' in x) else None, parse_table[0][-1])))):
        state.pop(0)
        state.append('InsideTab')
        print()
    elif state[0] == 'Accepted':
        state.pop(0)
        state.append('XXX')
        print()
    elif state[0] == 'Accepted2':
        state.pop(0)
        state.append('InsideTab')
        print()
    else:
        print('Syntax error in Line {}'.format(i+1))
        error += 1

if (error == 0):
    print('Compile success!')