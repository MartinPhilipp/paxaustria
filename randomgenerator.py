import random

e={}
for x in range(1000):
	w1=random.randint(1, 25)
	if w1 in e:
		e[w1]+=1
	else:
		e[w1]=1

sortlist=sorted(list(e.keys()))

print(sortlist)
for k in sortlist:
	print(k, e[k], e[k]*"/")


#2-----------------------------------

e={}
for x in range(1000):
	w2=int(random.gauss(22, 3))
	if w2 in e:
		e[w2]+=1
	else:
		e[w2]=1

sortlist=sorted(list(e.keys()))

print(sortlist)
for k in sortlist:
	print(k, e[k], e[k]*"?")
	

def wiederwurf(seiten=20):
	"""Würfle und bei höchster Zahl darf nochmal gewürfelt werden"""
	x=random.randint(1,seiten)
	if x < seiten:
		print(x)
		return x
	#x-=1
	print("PASCH",x)
	#x+=wiederwurf(seiten)
	return x+wiederwurf(seiten)-1
	
for y in range(10000):
	print("Ich kann würfeln! \(°⁻°)/",wiederwurf(20))
	
e={}
for x in range(100):
	w3=wiederwurf(6)
	if w3 in e:
		e[w3]+=1
	else:
		e[w3]=1

sortlist=sorted(list(e.keys()))

print(sortlist)
for k in sortlist:
	print(k, e[k], e[k]*"/")



