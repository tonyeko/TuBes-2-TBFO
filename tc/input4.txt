# TBFO x ITB x 2018 x Python x 3
x = open("aku_cinta_tbfo","r").readlines()

i = 0

while (i <= len(x)):
	if (x[i] is 'Aku cinta alstrukdat' and not(i == 99)):
		print('Mantap!')
		pass
	elif (True == False): # wut? ini apaan
		print('Does it even make sense?') 
		continue
	elif (x[i] == None):
		raise ErrorTBFO101 
		break
	i += 1

