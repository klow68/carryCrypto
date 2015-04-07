#ce programme n est pas en open source

def inverse_modulaire(a,b): #inverse de a modulo b

	#on cherche la forme r0 = r1 * a1 + r2
	r0 = a
	r1 = b
	r2 = 0
	a1 = 0
	start = 1
	cpt = 0
	a = []

	while r2 != 0 or start:
		if not start:
			r0 = r1
			r1 = r2
		else:
			start = 0

		cpt +=1
		a1 = int(r0 / r1)
		r2 = r0 % r1
		a.insert(cpt,a1)
		#print r0,"=",r1,"x",a1,"+",r2
	#print "M=",cpt
	#print a	

	#Valeurs arbitraires
	u0 = v1 = 1
	u1 = v0 = 0

	u = []
	u.insert(0,u0)
	u.insert(1,u1)

	v= []
	v.insert(0,v0)
	v.insert(1,v1)

	M = cpt
	cpt = 2
	while cpt <=M:
		u.insert(cpt, u[cpt - 2] - a[cpt-2]* u[cpt-1])
		cpt+=1
	
	#print u[M]
	return u[M]

	
		
	
print inverse_modulaire(75,28)	  