file = open("grammar/grammar1","r").read().replace("'''","").split("'")
file = list(filter(None, map(lambda x: x if (file.index(x)%2) else None, file)))
print(", ".join(file))