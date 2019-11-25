global EOP
global CC
global f
EOP = False
CC = ''
f = None

def ADV():
    CC = f.read(1)
    if (CC != ''):
        print(CC)
    else:
        EOP = True
    
def CLOSE():
    f.close()

def START(filename):
    global f
    f = open(filename, 'r')
    
if EOP:
    CLOSE()