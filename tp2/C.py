#! /usr/bin/python
#-*-coding: utf-8 -*-

import random
import sys
import math

def __pgcd(m,n):
	while m%n:
		r=m%n
		m=n
		n=r
	return n

def __search_s_and_d(n):
	s=1
	t = (n-1)/2
	while t%2 == 0:
		t = t/2
		s +=1

#liste des primitifs de n
def __primes(n):
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
def __lucas_lehmer(n,k = 7):
	# n>2
	if n<2:
		return False
	# le test de primalité de Lucas Lehmer ne marche que pour les nombre impairs
	if n==2:
		return True
	for _ in range(k):
		a = random.randint(3,n-2)
		if __exponentiation_modulaire_rapide(a,n-1,n) != 1:
			return False
		for q in __primes(n-1):
			if __exponentiation_modulaire_rapide(a,(n-1)/q,n) == 1:
				return False

	return True

def __exponentiation_modulaire_rapide(g,d,n):
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

def __inverse_modulaire(a,b):
	r = a
	r1 = b
	u = 1
	v = 0
	u1 = 0
	v1 = 1

	r = (a*u) + (b*v)
	r1 = (a*u1) + (b*v1)

	while r1 != 0:
		q = r/r1

		rs = r
		us = u
		vs = v

		r = r1
		u = u1
		v = v1

		r1 = rs - (q * r1)
		u1 = us - (q * u1)
		v1 = vs - (q * v1)

	while u <= 0:
		u = b + u
	#print a,b
	#print r,u,v
	return u


def __n_et_phi_de_n(p,q):
	n = p*q
	phi = (p-1)*(q-1)

	return [n,phi]

def __e_aleatoire(phi):
	d = random.randint(2,phi-1)
	while __pgcd(d,phi) != 1:
		d = random.randint(1,phi)
	return d

def __get_random():
	rand = random.randint(1000,10000)
	while not __lucas_lehmer(rand):
		rand = random.randint(1000,10000)

	return rand


def generation():

	p = __get_random()
	q = __get_random()

	n = p*q
	phi = (p-1)*(q-1)

	#e premier avec phi
	e = __e_aleatoire(phi)

	#print __pgcd(e,phi)

	d = __inverse_modulaire(e, phi)
	#d = 2753
	#print d
	x = d*e
	#print (d*phi)%n==1
	#test d correct
	#print __exponentiation_modulaire_rapide(x,1,n)==1

	return e,d,n



# excecute seulement si on lance C.py
if __name__ == '__main__':

	cle = generation()
	print "e : "+str(cle[0])
	print "d : "+str(cle[1])
	p = __get_random()
	q = __get_random()
	n = p*q
	phi = (p-1)*(q-1)
	print "---------"
