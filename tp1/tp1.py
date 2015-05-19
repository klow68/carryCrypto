#!/usr/bin/python
#-*-coding:utf8-*-

# fonction random
import random
# librairie permettant d'utiliser des pattern sur une chaine de texte
import re

NB_BIT = 5

dictionnaire = {'A': 0,'B':1,'C':2,'D':3,'E':4,
'F':5,'G':6,'H':7,'I':8,'J':9,
'K':10,'L':11,'M':12,'N':13,'O':14,
'P':15,'Q':16,'R':17,'S':18,'T':19,
'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25,' ':26,'.':27,',':28,'\'':29,'!':30,'?':31}

dic_bin = {dictionnaire[k]:k for k in dictionnaire.keys()}

def toilettage_binaire(binaire):
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
	msg_bin = encrypt_binaire(msg[0]) + encrypt_binaire(msg[1])
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
	# liste des caractères interdit
	if re.search("['\"²&é~#{}()\[\]\-|è`_\ç^à@°=+0-9]",mot):
		resultat = 1
		print "\n# Texte non valide : "+mot+"\n"
		
	return resultat


#******************************** EBC *********************************
print "\n# ECB encryption #\n"

mot='AAAA??BB'
mot = mot.upper()
mot=tailleTexteMod4(mot)
if verif_texte(mot)==1:
	exit(0)

print " Message   : "+mot

key='KXCX'
cypher_text=''
resultat =''
#save_mot = mot

#Encryption
for i in range (0,len(mot),4):
	cypher_text += encrypt_feistel(mot[:4],key);
	mot = mot[4:]

print "\n Chiffré : "+cypher_text


#Decryption
for i in range (0,len(cypher_text),4):
	resultat += decrypt_feistel(cypher_text[:4],key)
	cypher_text = cypher_text[4:]

print "\n Déchiffré : "+resultat+"\n"


#******************************** CBC *********************************

def vecteur_initialisation():
	length = len(dictionnaire) -1
	# 4 lettre random
	return dic_bin[random.randint(0,length)]+dic_bin[random.randint(0,length)]+dic_bin[random.randint(0,length)]+dic_bin[random.randint(0,length)]

def encrypt_CBC(mot,Key,VI):
	key = encrypt_mot_binaire(Key)
	res=''
	#print "encrypt"
	VI = encrypt_mot_binaire(VI)
	
	for i in range (0,len(mot),4):
		#passage des 4 premiers caractères en binaire
		plain_bin = encrypt_mot_binaire(mot[:4])
		#plain text XOR Vecteur d'initialisation
		cypher_text = ouExclusif(plain_bin[:20],VI)
		#passage en caractère 
		cypher_text = decrypt_mot_binaire(cypher_text)
		#print cypher_text
		cypher_text = encrypt_feistel(cypher_text,Key)

		res += cypher_text
		
		VI = encrypt_mot_binaire(cypher_text)

		#supression des 4 premier caractères déjà chiffrés
		mot = mot[4:]

	return res

def decrypt_CBC(mot,Key,VI):
	res=''
	VI = encrypt_mot_binaire(VI)

	for i in range (0,len(mot),4):
		#passage des 4 premier caractère en binaire
		cipher_text = decrypt_feistel(mot[:4],Key)

		cipher_text = ouExclusif(encrypt_mot_binaire(cipher_text),VI) 

		res += decrypt_mot_binaire(cipher_text)
		
		VI = encrypt_mot_binaire(mot[:4])

		#supression des 4 premier caractère déjà crypter
		mot = mot[4:]

	return res



print "\n# CBC encryption #\n"

crypt=''
decrypt=''

mot='Je suis une phrase'
mot = mot.upper()
mot=tailleTexteMod4(mot)
if verif_texte(mot)==1:
	exit(0)

key='KXCX'

#VI = vecteur_initialisation()
VI="PROU"

print " Vect Init : "+VI

print "\n Message   : "+mot

crypt = encrypt_CBC(mot,key,VI)

print "\n Encrypter : "+crypt

decrypt = decrypt_CBC(crypt,key,VI)

print "\n Decrypter : "+decrypt+"\n"


