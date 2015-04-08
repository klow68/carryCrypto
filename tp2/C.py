#! /usr/bin/python
#-*-coding: utf-8 -*-

import random
import sys
import math

def pgcd(m,n):
	while m%n:
		r=m%n
		m=n
		n=r
	return n

def search_s_and_d(n):
	s=1
	t = (n-1)/2
	while t%2 == 0:
		t = t/2
		s +=1

#liste des primitifs de n
def primes(n):
    prime = []
    d = 2
    while d*d <= n:
        while (n % d) == 0:
            prime.append(d)
            n //= d
        d += 1
    if n > 1:
       prime.append(n)
    return prime

#Test de primatlité
def lucas_lehmer(n,k = 7):
	# n>2
	if n<2:
		return False
	# le test de primalité de Lucas Lehmer ne marche que pour les nombre impairs
	if n==2:
		return True
	for _ in range(k):
		a = random.randint(3,n-2)
		if exponentiation_modulaire_rapide(a,n-1,n) != 1:
			return False
		for q in primes(n-1):
			if exponentiation_modulaire_rapide(a,(n-1)/q,n) == 1:
				return False

	return True

def exponentiation_modulaire_rapide(g,d,n):
	d = bin(d)
	# supprime les caractère "0b"
	d = d[2:]
	# reverse la chaine
	d = d[::-1]

	R0 = 1
	R1 = g
	for i in range(len(d)):
		if d[i]=="1":
			R0 = (R1*R0) % n
		R1 = (R1**2) % n
	return R0


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

def n_et_phi_de_n(p,q):
	n = p*q
	phi = (p-1)*(q-1)

	return [n,phi]

def e_aleatoire(phi):
	d = random.randint(2,phi-1)
	while pgcd(d,phi) != 1:
		d = random.randint(1,phi)
	return d

	
rand = random.randint(1000,10000)	
while not lucas_lehmer(rand):
	rand = random.randint(1000,10000)

print rand

print inverse_modulaire(75,28)	  

print exponentiation_modulaire_rapide(41,37,527)

print e_aleatoire(60)


