#! /usr/bin/python
#-*-coding: utf-8 -*-

import random
import sys
import math
NB_BIT = 5
dictionnaire = {'A': 0,'B':1,'C':2,'D':3,'E':4,
'F':5,'G':6,'H':7,'I':8,'J':9,
'K':10,'L':11,'M':12,'N':13,'O':14,
'P':15,'Q':16,'R':17,'S':18,'T':19,
'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25,' ':26,'.':27,',':28,'\'':29,'!':30,'?':31}

dic_bin = {dictionnaire[k]:k for k in dictionnaire.keys()}

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
	# supprime les caractères "0b"
	d = d[2:]
	# renverse la chaine
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




#-----------------Importation des fonctions du TP1-----------------#

def toilettage_binaire(binaire):
	#jean_nono
	taille = len(binaire) - 2
	cypherText=''
	if(taille < NB_BIT):
		for j in range(NB_BIT-taille):
			cypherText+='0'

	for i in range(2,taille+2):
		cypherText+= binaire[i]

	return cypherText

def encrypt_binaire(lettre):
	return toilettage_binaire(bin(dictionnaire[lettre]))
def encrypt_mot_binaire(mot):
	mot_bin = ''
	for i in mot:
		mot_bin += encrypt_binaire(i)
	return mot_bin
def decrypt_binaire(binaire):
	#return dictionnaire[int(binaire,2)]
	dic_bin[(int(binaire,2))]
	return dic_bin[(int(binaire,2))]

def decrypt_mot_binaire(mot_bin):
	mot=''
	for i in range(0,len(mot_bin),5):
		mot+=decrypt_binaire(mot_bin[:5])
		mot_bin=mot_bin[5:]

	return mot

def function(msg,Key):
	#Decalage binaire
	msg_bin = encrypt_mot_binaire(msg)
	#print msg_bin
	msg_fin=''
	for i in range(1,len(msg_bin)):
		msg_fin+= msg_bin[i]
	msg_fin+=msg_bin[0]
	#print msg_fin
	#ou exclusif
	return ouExclusif(msg_fin,Key)

def ouExclusif(A,B):
	resultat = ''
	for i in range(0,len(A)):
		if (A[i] == B[i] and B[i]=='1'):
			resultat += '0'
		elif A[i] == '1' or B[i]=='1':
			resultat += '1'
		else:
			resultat += '0'
	return resultat

def encrypt_feistel(bloc,Key):
	G = bloc[:2]
	D = bloc[2:]
	#print "encrypt"
	for i in range(4):
		#copie du bloc de droite
		D2 = D
		#la cle prend les deux premiers caracteres
		Key_feistel = Key[:2]
		#La cle globale est décalée de 1 caractere
		Key = Key[1:]+Key[:1]
		#On chiffre la partie droite
		#print "key:"+Key_feistel
		print G+" : "+D +" ////////// "+Key_feistel 

		D = function(D,encrypt_mot_binaire(Key_feistel))
		
		#Maintenant, il faut réaliser le ou exclusif
		D = decrypt_mot_binaire(ouExclusif(D,encrypt_mot_binaire(G)))
		G = D2

		print G+" : "+D
		print Key_feistel

	return G+D
def encrypt_feistel_2(bloc,key):
	key_blocs = []
	for i in range(0,len(key)):
		if(i<len(key)-1):
			if(i<len(key)-2):
				key_blocs.append(str(key[i])+str(key[i+1])+str(key[i+2]))
			else:
				key_blocs.append(str(key[i])+str(key[i+1])+str(key[0]))
		else:
			key_blocs.append(str(key[i])+str(key[0])+str(key[1]))
				
	while len(bloc) % (len(key_blocs[0])) > 0:
		tmp  = "A"
		tmp += bloc
		bloc = tmp

	print bloc
	G = bloc[:len(key_blocs[0])]
	D = bloc[len(key_blocs[0]):]
	for i in range(len(key_blocs)):
		print key_blocs[i]
		D2 = D
		D = function(D,encrypt_mot_binaire(key_blocs[i]))
		D = decrypt_mot_binaire(ouExclusif(D,encrypt_mot_binaire(G)))
		G = D2
	return D+G

def decrypt_feistel_2(bloc,key):
	key_blocs = []
	for i in range(0,len(key)):
		if(i<len(key)-1):
			if(i<len(key)-2):
				key_blocs.append(str(key[i])+str(key[i+1])+str(key[i+2]))
			else:
				key_blocs.append(str(key[i])+str(key[i+1])+str(key[0]))
		else:
			key_blocs.append(str(key[i])+str(key[0])+str(key[1]))
				
	while len(bloc) % (len(key_blocs[0])) > 0:
		tmp  = "A"
		tmp += bloc
		bloc = tmp

	G = bloc[:len(key_blocs[0])]
	D = bloc[len(key_blocs[0]):]
	for i in range(len(key_blocs)-1,-1,-1):
		D2 = D
		D = function(D,encrypt_mot_binaire(key_blocs[i]))
		D = decrypt_mot_binaire(ouExclusif(D,encrypt_mot_binaire(G)))
		G = D2
	while (D[0]=='A'):
		tmp = D[len(D)-1:]
		D = tmp
	return D+G
def decrypt_feistel(bloc,Key):
	D = bloc[:2]
	G = bloc[2:]
	Key = Key[3:]+Key[:3]
	#print Key
	#print "Decrypt"
	for i in range(4):
		#copie du bloc de droite
		D2 = D
		#la cle prend les deux premiers caracteres
		Key_feistel = Key[:2]
		#La cle globale est décalée de 1 caractere
		Key = Key[3:]+Key[:3]
		#print Key
		#On chiffre la partie droite
		#print "key:"+Key_feistel
		D = function(D,encrypt_mot_binaire(Key_feistel))
		
		#Maintenant, il faut réaliser le ou exclusif
		D = decrypt_mot_binaire(ouExclusif(D,encrypt_mot_binaire(G)))
		G = D2

	return D+G

def tailleTexteMod4(mot):
	space=''
	if len(mot)%4 != 0:
		nb_space =4-len(mot)%4
		for i in range(nb_space):
			space+=' '
	return mot+space

def verif_texte(mot):
	resultat = 0
	# liste des caractères interdits
	if re.search("['\"²&é~#{}()\[\]\-|è`_\ç^à@°=+0-9]",mot):
		resultat = 1
		print "\n# Texte non valide : "+mot+"\n"
		
	return resultat

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
