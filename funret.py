def add(a ,b):
	print "Adding %d + %d" %(a, b)
	return a + b

def sub(a, b):
	print "Subing %d - %d" %(a, b)
	return a - b

def multi(a, b):
	print "Multi %d * %d" %(a, b)
	return a * b

def divi(a, b):
	print "Divi %d / %d" %(a, b)
	return a / b

print "Do some function!"

age = add(2, 10)
height = sub(1, 0)
weight = multi(age, height)
iq = divi(100, 3)

print '%d %d %d %d' %(age, height, weight, iq)
