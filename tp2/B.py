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
rand=""
mdp=""

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

def envoie_message_to_A(msg):
	print "\n  $$ Message à chiffrer : "+msg
	# Demande a A ça clé public
	cle_A = a.get_cle_publique()
	msg_crypter = []
	for caract in msg:
		msg_crypter.append(__exponentiation_modulaire_rapide(toInt(caract),int(cle_A[0]),int(cle_A[1])))
	print "\n  $$ Envoie du message chiffré à A : "+str(msg_crypter)
	return msg_crypter

def decrypt_message_from_A(msg_crypt):
	global d
	global n
	msg = ''
	for caract in msg_crypt:
		msg += toLetter(__exponentiation_modulaire_rapide(caract, d, n))

	print "\n  $$ Message déchiffré par B : "+msg
	return msg

def etape_1(msg_crypt):
	msg_decrypt = decrypt_message_from_A(msg_crypt)
	etape_2(msg_decrypt)

def etape_2(msg):
	print "\n  ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤ 2 ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤"
	if msg == "AB ?!":
		msg_ok = "AB OK"
		msg_crypt = envoie_message_to_A(msg_ok)
		a.etape_2(msg_crypt)

def etape_3(msg_crypt):
	global rand
	rand = decrypt_message_from_A(msg_crypt)
	msg_crypt = envoie_message_to_A(rand)
	a.etape_3_suite(msg_crypt)
def etape4(msg_decrypt):
	if msg_decrypt == rand:
		msg = "AB OK"
		msg_droite = msg[-len(rand):]
		msg_droite_bin = c.encrypt_mot_binaire(msg_droite)
		global mdp
		mdp += c.encrypt_binaire(msg[:len(msg)-len(rand)])
		mdp += c.ouExclusif(msg_droite_bin,c.encrypt_mot_binaire(rand))
		mdp = c.decrypt_mot_binaire(mdp)
		print "\n$$ Mot de passe " +mdp
		a.etape_5()

def etape_6(msg_chiffre):
	print "\n  ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤ 6 ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤"
	print "\n$$Dechiffrage de " + msg_chiffre

	code = c.decrypt_feistel_2(msg_chiffre,mdp)
	print "\n$$ Message lu : " + code

# petit tour pour régler le problème d'import circulaire de python
def main():
	a.etape_1()

# excecute seulement si on lance B.py
if __name__ == '__main__':
	#a.generation()
	#generation()
	#print "\n Clés de B : "
	#print "  # e : "+str(e)
	#print "  # d : "+str(d)
	#print "  # n : "+str(n)
	#a.decrypt_message_from_B(envoie_message_to_A(['A','C']))
	print "$$$ A commence la communication $$$"
	a.main()

