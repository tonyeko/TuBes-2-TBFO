import string

all_chars = string.ascii_uppercase+string.ascii_lowercase+string.digits+'_'

#open("grammar1.dat", "r")
with open("grammar1.dat", "w") as f:
	X = ""
	for i in range(len(all_chars)):
		f.write('Chr'+all_chars[i]+' -> '+all_chars[i]+'\n')
		X += all_chars[i] + " | "
	f.write('ChrVar -> '+X[:-2]+'\n')
	X = ""
	for i in range(len(string.printable[:-6])):
		X += string.printable[i] + " | "
	f.write('Chr -> '+X[:-2]+'\n')