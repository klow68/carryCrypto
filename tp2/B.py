#! /usr/bin/python
#-*-coding: utf-8 -*-

import random
import sys
import math
import C as c
import A as a

dictionnaire = {'A': 0,'B':1,'C':2,'D':3,'E':4,
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
	return e

def envoie_message_to_B(msg,n):
	cle_A = a.get_cle_publique()
	msg_crypter = __exponentiation_modulaire_rapide(msg,cle_A,n)
	return msg_crypter

# excecute seulement si on lance B.py
if __name__ == '__main__':	
	generation()
	print "e : "+str(e)
	print "d : "+str(d)
	print "n : "+str(n)