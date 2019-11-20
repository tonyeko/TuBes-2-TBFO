with open(r'chowsky', 'r') as infile, open(r'chowskynopetik', 'w') as outfile:
    data = infile.read()
    data = data.replace("'", "")
    outfile.write(data)