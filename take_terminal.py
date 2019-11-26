print('List of terminals:')
file = open("grammar/grammar1","r").read().replace("'''","").split("'")
file = list(dict.fromkeys(filter(None, map(lambda x: x if (file.index(x)%2) else None, file))))
print(", ".join(file) + ", '")

print()

print('List of variables:')
file = open("grammar/grammar1","r").readlines()
file = list(dict.fromkeys(filter(None, map(lambda x: x.replace('\n','').split(" ")[0], file))))
print(", ".join(file))