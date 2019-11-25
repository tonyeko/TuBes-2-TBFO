from collections import defaultdict
import itertools
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
            for x in list(map(lambda x: x[0][1:-1] if (len(x) == 1) else "".join(x), map(lambda x: x.split(" "), rule.right))):
                try:
                    self.rules[x].append(rule.left)
                except:
                    self.rules[x] = [rule.left]
        #print(self.rules)
        #exit()

def search_rules(grammar, right):
    matches = []
    try:
        matches = grammar.rules["".join(right)]
    except:
        matches = []
    return matches

def recur_search(prods, grammar):
    #print(prods)
    if (len(prods) == 1):
        return search_rules(grammar, prods[0])
    elif (len(prods) == 2):
        a = []
        for i in list(itertools.product(list(filter(None,search_rules(grammar,prods[0]))),list(filter(None,search_rules(grammar,prods[1]))))):
            a.append(search_rules(grammar,"".join(i)))
        a = list(filter(None,a))
        #print(a[0])
        return a[0]
    else:
        a = []
        for i in list(itertools.product(search_rules(grammar,prods[0]),recur_search(prods[1:],grammar))):
            #print(i)
            a.append(search_rules(grammar, "".join(i)))
        return list(filter(None,a))[0]
        

def parse(sentence, grammar):
    # print("=========================")
    print(sentence)
    # print("=========================")
    # words = [i for i in sentence]
    # word = sentence.split()                                 # Hilangin spasi

    word = sentence.split("'")
    if (len(word)%2 == 0):
        word = ['^','%']
    else:
        word = list(map(lambda x: 'a' if (word.index(x)%2) else x, word))
        word = "'".join(word).split()

    # INI UNTUK KASUS OPERATOR
    word2 = re.split('[-+*/]', ''.join(word))               # hilangin simbol operator
    for i in range(len(word)):
        for j in range(len(word2)):
            if word[i] == word2[j]:
                word[i] = 'x'
    # print(words)
    words = ''.join(word)
    print(words)

    for i in range(len(words)):
        #print(words[i], end=" ")
        if words[i] == ' ':
            words[i] = '~'          # Kalau dimasukkin ke line.replace ngeprintnya jadi jelek
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
        table[column][column] = search_rules(grammar, [words[column]])
        for row in reversed(range(column + 1)):
            for s in range(row + 1, (column + 1)):
                for non_term in itertools.product(table[row][s - 1], table[s][column]):
                        table[row][column].extend(search_rules(grammar, non_term))
    '''
    for column in range(len(words)):
        table[column][column] = search_rules(grammar, [words[column]])
        #print(table[column][column])
    '''

    # Algoritma 2
    '''
    if (len(words) == 1):
        table[0][len(table)-1] = search_rules(grammar, words)
    else:
        table[0][len(table)-1] = [j for i in filter(None, map(lambda x: search_rules(grammar, x), itertools.product(search_rules(grammar, [words[-2]]),search_rules(grammar, [words[-1]])))) for j in i]
    print(table[0][len(table)-1])
    i = len(words)-3
    while (i >= 0):
        #print(table[0][len(table)-1])
        table[1][len(table)-1] = [j for k in filter(None, map(lambda x: search_rules(grammar, x), itertools.product(search_rules(grammar, [words[i]]), table[0][len(table)-1]))) for j in k]
        if (table[1][len(table)-1] == []):
            i -= 1
    '''

    #print(table[0][len(table)-1])
    #print(table[0][len(table)-1])
    for i in table[0][len(table)-1]:
        #print(i, state[0])
        if state[0] in i:
            state.pop(0)
            state.append('Accepted2')
            break
        elif i == 'S':
            state.pop(0)
            state.append('Accepted')
            break

    return table

import time
x = time.time()

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
    '''
    for row in range(len(parse_table)):
        for col in range(len(parse_table)):
            print(parse_table[row][col], end="")
        print()
    '''
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

print(time.time()-x)