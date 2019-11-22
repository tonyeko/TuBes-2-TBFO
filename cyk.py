def parse(program, grammar):
    length = len(program)
    
    parse_table = [[[] for x in range(length - y)] for y in range(length)]

    for i, word in enumerate(program):
        for rule in grammar:


