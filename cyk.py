from collections import defaultdict
import itertools
import re
import time

GRAMMAR_RULES = "./grammar/chowsky"
SENTENCES = input("Masukkan nama file yang ingin diuji: ")

blacklisted = {
    'else': '',
    'if': '',
    'def': '',
    'elif': '',
    'class': '',
    'import': '',
    'from': '',
    'for': '',
    'while': '',
    'in': '',
    'return': '',
    'with': '',
    'as': '',
    'is': '',
    'and': '',
    'or': '',
    'raise': ''
}

def read_grammar(filename):
    all_lines = list()
    with open(filename, "r") as file:
        for line in file.readlines():
            all_lines.append(line.replace("\n", ""))
    return all_lines

def read_python_file(filename):
    all_lines = list()
    file = ''.join(removecomment(open(filename, "r").read()))
    file1 = open("temp","w"); file1.write(file); file1.close()
    with open('temp', "r") as file:
        for line in file.readlines():
            all_lines.append(line.replace("\n", ";").replace("\t", "$"))
    return all_lines

def removecomment(sentence):
    temp = sentence.split("\n")
    idxpetik = []
    for i in range(len(temp)):
        if "'''" in temp[i]:
            idxpetik.append(i)
    i = 0
    while (i < len(idxpetik)):
        try:
            for j in range(idxpetik[i],idxpetik[i+1]+1):
                temp[j] = ""
        except:
            for j in range(idxpetik[i],len(temp)):
                temp[j] = "^%"
        i += 2
    return '\n'.join(temp)

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
        
def splitquote(sentence, quote):
    word = sentence.split(quote)
    if (len(word)%2 == 0):
        word = ['^', '%']
    else:
        word = list(map(lambda x: 'a' if (word.index(x)%2) else x, word))
        word = '"'.join(word).split(' ')
    return word

def parse(sentence, grammar):
    word = " ".join(splitquote(sentence.rstrip(), "'"))
    word = " ".join(splitquote(word, '"'))
    words = list(word)

    for i in range(len(words)):
        if words[i] == ' ':
            words[i] = '~'
    
    # Algoritma 1
    if (len(words) >= 2 and words[0] == '~'):
        while (words[1] == '~'):
            words.pop(1)
    if  ('#' in "".join(words)):
        i = words.index('#')
        while (i < len(words)):
            words.pop(i)
        words.append(';')

    # Algoritma 2
    if (len(words) > 0):
        column = 0
        while(column < len(words)):
            if (words[column] == '~'):
                while (column < len(words)-1 and words[column+1] == '~'):
                    words.pop(column+1)
            temp = search_rules(grammar, [words[column]])
            if ('Var' in temp):
                temp = search_rules(grammar, [words[column]])
                a = 1
                while(column+a < len(words)-1 and 'VarKons' in temp):
                    temp = search_rules(grammar, [words[column+a]])
                    a += 1
                x = "".join(words[column:column+a-1])
                try:
                    blacklisted[x]
                    column += a-1
                except:
                    [words.pop(column+1) for i in range(a-2)]
            elif ('Angka' in temp):
                temp = search_rules(grammar, [words[column]])
                a = 1
                while(column+a < len(words)-1 and 'Angka' in temp):
                    temp = search_rules(grammar, [words[column+a]])
                    a += 1
                [words.pop(column+1) for i in range(a-2)]
            column += 1
        temp = words.copy()
        temp2 = "".join(words).replace('$','').replace(':','').replace(';','').split("~")
        if (len(co) and ('for' in temp2 or 'while' in temp2 or 'with' in temp2 or 'else' in temp2 or 'elif' in temp2 or 'if' in temp2 or 'def' in temp2 or 'class' in temp2) and temp[0] == '$'):
            while (temp[0] == '$'):
                temp.pop(0)
            words = temp.copy()
        elif (len(co) > 1):
            x = "".join(words).count('$')-1
            while (x > 0):
                if (temp[0] == '$'):
                    temp.pop(0)
                    x -= 1
                else:
                    break
            if (x == 0):
                words = temp.copy()

    # Algoritma 3
    table = [ [ [] for i in range(len(words)) ] for j in range(len(words)) ] 
    for column in range(len(words)):
        table[column][column] = search_rules(grammar, [words[column]])
        for row in reversed(range(column + 1)):
            for s in range(row + 1, (column + 1)):
                for non_term in itertools.product(table[row][s - 1], table[s][column]):
                        table[row][column].extend(search_rules(grammar, non_term))

    # Algoritma 4
    for i in table[0][-1]:
        if state[-1] == i:
            if (len(co) == sentence.count('$')):
                ooo[0] += 1
            state.pop(0)
            state.append('Accepted2')
            break
        elif i == 'S':
            state.pop(0)
            state.append('Accepted')
            break
    return table

try:
    print("Starting the compiling process...")
    starttime = time.time()
    grammar = read_grammar(GRAMMAR_RULES)
    sentences = read_python_file(SENTENCES)
    realtext = list(map(lambda x: x.replace('\n',''), open(SENTENCES, "r").readlines()))
    grammar = Grammar(grammar)
    state = ['XXX']
    co = []
    ooo = [-1]
    errorLines = []
    for i in range(len(sentences)):
        parse_table = parse(sentences[i], grammar)
        a = 0
        for j in parse_table[0][-1]:
            if (sentences[i].replace('$','').replace(';','').replace(' ','') != "" and not('HeadIf' in j or 'HeadElif' in j or 'HeadFor' in j or 'HeadWhile' in j or 'HeadFungsi' in j or 'HeadClass' in j or 'HeadWith' in j or 'HeadElse' in j) and len(co) > sentences[i].count('$') and not(ooo[0])):
                if (state[-1] == 'Accepted'):
                    state.pop(-1)
                    state.append('InsideTab')
                break
            elif (sentences[i].replace('$','').replace(';','').replace(' ','') == ""):
                a += 1
                break
            elif (len(co) >= sentences[i].count('$') and 'HeadIf' in j):
                [co.pop(-1) for i in range(len(co)-sentences[i].count('$'))]
                if (len(co) == 0):
                    state.pop(-1)
                state.append('InsideTab')
                co.append('IF')
                ooo[0] = 0
                a += 1
                break
            elif (len(co) >= sentences[i].count('$') and 'HeadFor' in j):
                [co.pop(-1) for i in range(len(co)-sentences[i].count('$'))]
                if (len(co) == 0):
                    state.pop(-1)
                state.append('InsideTab')
                co.append('For')
                ooo[0] = 0
                a += 1
                break
            elif (len(co) >= sentences[i].count('$') and 'HeadWhile' in j):
                [co.pop(-1) for i in range(len(co)-sentences[i].count('$'))]
                if (len(co) == 0):
                    state.pop(-1)
                state.append('InsideTab')
                co.append('While')
                ooo[0] = 0
                a += 1
                break
            elif (len(co) >= sentences[i].count('$') and 'HeadFungsi' in j):
                [co.pop(-1) for i in range(len(co)-sentences[i].count('$'))]
                if (len(co) == 0):
                    state.pop(-1)
                state.append('InsideTab')
                co.append('Fungsi')
                ooo[0] = 0
                a += 1
                break
            elif (len(co) >= sentences[i].count('$') and 'HeadClass' in j):
                [co.pop(-1) for i in range(len(co)-sentences[i].count('$'))]
                if (len(co) == 0):
                    state.pop(-1)
                state.append('InsideClass')
                co.append('Class')
                ooo[0] = 0
                a += 1
                break
            elif (len(co) >= sentences[i].count('$') and 'HeadWith' in j):
                [co.pop(-1) for i in range(len(co)-sentences[i].count('$'))]
                if (len(co) == 0):
                    state.pop(-1)
                state.append('InsideTab')
                co.append('With')
                ooo[0] = 0
                a += 1
                break
            elif (len(co) and 'Fungsi' in co and 'InsideReturn' in j):
                ooo[0] += 1
                a += 1
            elif (len(co) and 'HeadElif' in j and 'IF' == co[-1] and sentences[i].count('$') == len(co)-1):
                a += 1
                break
            elif (len(co) and 'HeadElif' in j and sentences[i].count('$') < len(co)-1 and 'IF' == co[sentences[i].count('$')]):
                [state.pop(-1) for i in range(len(co)-sentences[i].count('$'))]
                [co.pop(-1) for i in range(len(co)-sentences[i].count('$')-1)]
                a += 1
                break
            elif (len(co) and 'HeadElse' in j and 'IF' == co[-1] and sentences[i].count('$') == len(co)-1):
                co.pop(-1)
                co.append('ELSE')
                a += 1
                break
            elif (len(co) and 'HeadElse' in j and sentences[i].count('$') < len(co)-1 and 'IF' == co[sentences[i].count('$')]):
                [state.pop(-1) for i in range(len(co)-sentences[i].count('$')-1)]
                [co.pop(-1) for i in range(len(co)-sentences[i].count('$'))]
                co.append('ELSE')
                a += 1
                break
            elif (state[-1] == 'Accepted'):
                [state.pop(-1) for i in range(len(co)-sentences[i].count('$'))]
                if (len(state)):
                    state.pop(-1)
                state.append('XXX')
                if (co != []):
                    [co.pop(-1) for i in range(len(co)-sentences[i].count('$'))]
                a += 1
                break
            elif (state[-1] == 'Accepted2' and sentences[i].count('$') <= len(co)):
                state.pop(-1)
                state.append('InsideTab')
                if (co != []):
                    [co.pop(-1) for i in range(len(co)-sentences[i].count('$'))]
                a += 1
                break
        if (len(co) and sentences[i].count('$')):
            state.pop(-1)
            state.append('InsideTab')
        if (i == len(sentences)-1 and len(co) and ooo[0] == 0 and a != 0):
            a = 0
        if (a == 0):
            errorLines.append(i)
    print()
    if (len(errorLines) == 0):
        print('Compile success!')
    else:
        for i in errorLines:
            print(realtext[i] + '  ' + 'Syntax Error in Line ' + str(i))
    print()
    print("Compiling time: {:5f} s".format(time.time()-starttime))
except:
    print("ERROR BACA FILE")