#!/usr/bin/python
#-*-coding:utf8-*-

NB_BIT = 5

dictionnaire = {'A': 0,'B':1,'C':2,'D':3,'E':4,
'F':5,'G':6,'H':7,'I':8,'J':9,
'K':10,'L':11,'M':12,'N':13,'O':14,
'P':15,'Q':16,'R':17,'S':18,'T':19,
'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25,' ':26,'.':27,',':28,'\'':29,'!':30,'?':31}

dic_bin = {dictionnaire[k]:k for k in dictionnaire.keys()}

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

def decrypt_binaire(binaire):
	#return dictionnaire[int(binaire,2)]
	dic_bin[(int(binaire,2))]
	print dic_bin[(int(binaire,2))]

def function(msg,Key):
	#Decalage binaire
	msg_bin = encrypt_binaire(msg[0]) + encrypt_binaire(msg[1])
	print msg_bin
	msg_fin=''
	for i in range(1,len(msg_bin)):
		msg_fin+= msg_bin[i]
	msg_fin+=msg_bin[0]
	print msg_fin
	#ou exclusif
	msg_tmp = ''
	for i in range(0,len(msg_fin)):
		if (msg_fin[i] == Key[i] and Key[i]=='1'):
			msg_tmp += '0'
		else:
			msg_tmp += msg_fin[i]
	return msg_tmp

decrypt_binaire( encrypt_binaire('Z'))
print function('ZB','0000000000')
	
