#! /usr/bin/python
#-*-coding: utf-8 -*-

import random
import sys
import math
import C as c
import B as b

dictionnaire = {'A': 32,'B':33,'C':2,'D':3,'E':4,
'F':5,'G':6,'H':7,'I':8,'J':9,
'K':10,'L':11,'M':12,'N':13,'O':14,
'P':15,'Q':16,'R':17,'S':18,'T':19,
'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25,' ':26,'.':27,',':28,'\'':29,'!':30,'?':31}

dic_bin = {dictionnaire[k]:k for k in dictionnaire.keys()}

e = ""
d = ""
n = ""

def generation():
	global e
	global d
	global n
	cle = c.generation()
	e= cle[0]
	d = cle[1]
	n = cle[2]

def toInt(lettre):
	return dictionnaire[lettre]

def toLetter(num):
	return dic_bin[num]

def toASCII(nombre):
	return int(dic_bin[nombre])
	
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

def get_cle_publique():
	return e,n

def envoie_message_to_B(msg):
	cle_B = b.get_cle_publique()
	print cle_B
	msg_crypter = []
	for caract in msg:
		msg_crypter.append(__exponentiation_modulaire_rapide(toInt(caract),int(cle_B[0]),int(cle_B[1])))
	return msg_crypter

def decrypt_message_from_B(msg_crypt):
	global d
	global n
	msg = ''
	for caract in msg_crypt:
		msg += toLetter(__exponentiation_modulaire_rapide(caract, d, n))
	return msg

# excecute seulement si on lance B.py
if __name__ == '__main__':
	b.generation()
	generation()
	print "e : "+str(e)
	print "d : "+str(d)
	print "n : "+str(n)
	print b.decrypt_message_from_A(envoie_message_to_B(['A','B']))
