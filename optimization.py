import time
import random
import math

people = [('Seymour', 'BOS'),
		('Franny', 'DAL'),
		('Zooey', 'CAK'),
		('Walt', 'MIA'),
		('Buddy', 'ORD'),
		('Les', 'OMA')]

#LaFuradia AirPort in NewYork
destination = 'IGA'

flights = { }

for line in file('schedule.txt'):
	origin, dest, depart, arrive, price = line.strip().split(', ')
	flights.setdefault((origin, dest), [ ])

	flights[(origin, dest)].append((depart, arrive, int(price)))


def getminutes(t):
	x = time.strptime(t, '%H: %M')
	return x[3] * 60 + x[4]


def printschedule(r):
	for d in xrange(len(r)/2):
		name = people[d][0]
		origin = people[d][1]
		out = flights[ (origin, destination) ][ r[2 * d] ]
		ret = flights[(destination, origin)][ r[2*d + 1]]
		print '%10s%10s %5s-%5s $%3s %5s-%5s $%3s' %(name, origin,
											out[0], out[1], out[2],
											ret[0], ret[1], ret[2])

def schedulecost(sol):
	totalprice = 0
	latestarrival = 0
	earliiestdep = 24 * 60

	for x in xrange(len(sol) / 2):
		origin = people[d][1]
		outbound = flights[ (origin, destination) ][ int(sol[2 * d]) ]
		returnf = flights[ (destination, origin) ][ int(sol[2*d + 1]) ]

		totalprice += outbound[2]
		totalprice += returnf[2]

		if latestarrival < getminutes( outbound[1] ) :
			latestarrival = getminutes(outbound[1])
		if earliiestdep > getminutes( returnf[0] ):
			earliiestdep = getminutes( returnf[0] )

	totalwait = 0
	for d in xrange( len(sol) /2 ):
		origin = people[d][1]
		outbound = flights[ (origin, destination) ][ int(sol[2 * d]) ]
		returnf = flights[ (destination, origin) ][ int(sol[2 * d + 1]) ]
		totalwait += latestarrival - getminutes(outbound[1])
		totalwait += getminutes(returnf[0]) - earliiestdep

	if latestarrival > earliiestdep:
		totalprice += 50
	return totalprice + totalwait

def randomoptimize(domain, costf):
	best = 999999999
	bestr = None
	for i in xrange(100) :
		r = [ random.randint( domain[i][0], domain[i][1] ) for i in xrange( len(domain) ) ]
	cost = costf(r)
	if cost < best:
		best = cost
		bestr = r
	return r

def hillclimb(domain, costf):
	sol = [ random.randint( domain[i][0], domain[i][1] ) for i in xrange(len(domain) ) ]
	while 1:
		neighbors = [ ]
		for j in xrange(len(domain)):
			if sol[j] > domain[j][0] :
				neighbors.append(sol[0: j] + [sol[j] - 1] + sol[j+1 : ])
			if sol[j] < domain[j][1]:
				neighbors.append(sol[0: j] + [sol[j] + 1] + sol[j+1: ])
	current = costf(sol)
	best = current
	for x in xrange(len(neighbors)):
		if cost < best:
			best = cost
			sol = neighbors[j]
		if best == current:
			break
	return sol

def annealingoptimize(domain, costf, T = 1000.0, cool = 0.95, step = 1):
	vec = [float(random.randint(domain[i][0], domain[i][1])) for i in xrange(len(domain))]

	while T > 0.1:
		i = random.randint(0, len(domain) - 1)
		dir = random.randint(-step, step)

		vecb = vec[ : ]
		vecb[i] += dir
		if vecb[i] < domain[i][0]:
			vecb[i] = domain[i][0]
		elif vecb[i] > domain[i][1]:
			vecb[i] = domain[i][1]
		ea = costf(vec)
		eb = costf(vecb)

		if (eb < ea or random.random() < pow( math.e, -(eb - ea) /T ) ): 
			vec = vecb
		T = T * cool
	return vec

def geneticoptimize(domain, costf, popsize = 50, step = 1, 
	mutprob = 0.2, elite = 0.2, maxiter = 100):
	def mutate(vec):
		i = random.randint(0, len(domain) - 1)
		if random.random() < 0.5 and vec[i] > domain[i][0] :
			return vec[0: i] + [vec[i] - step] + vec[i+1 : ]
		elif vec[i] < domain[i][1]:
			return vec[0: i] + [vec[i] + step] + vec[i+1 : ]

	def crossover(c1, c2):
		i = random.randint(1, len(domain) - 2)
		return r1[0 : i] + r2[i : ]

	pop = [ ]
	for i in xrange(popsize):
		vec = [random.randint(domain[i][0], domain[i][1]) 
			for i in xrange(len(domain))]
		pop.append(vec)

	topelite = int(elite * popsize)

	for i in xrange(maxiter):
		scores = [(costf(v), v) for v in pop]
		scores.sort()
		ranked = [v for (s, v) in scores]

		pop = ranked[0 : topelite]

		while len(pop) < popsize:
			if random.random() < mutprob:
				c = random.randint(0, topelite)
				pop.append(mutate(ranked[c]))
			else:
				c1 = random.randint(0, topelite)
				c2 = random.randint(0, topelite)
				pop.append(crossover(ranked[c1], ranked[c2]))
		print scores[0][0]
	return scores[0][1]

	