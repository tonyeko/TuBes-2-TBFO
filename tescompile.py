    word = sentence.split(quote)
    if (len(word)%2 == 0):
        word = ['^', '%']
    else:
        word = list(map(lambda x: 'a' if (word.index(x)%2) else x, word))
        word = '"'.join(word).split(' ')