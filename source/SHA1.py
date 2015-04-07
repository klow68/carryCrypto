import array
from math import floor
import sys


# 2^32 en HEXA
N = 0x100000000;

# 2^32 - 1 
MASK = 	0xFFFFFFFF;


#  Fonction :  Decallage a gauche de n bit , d'un mot de 32 bit word
def leftRotate(word, n):
	return ((word<<n)&MASK)|(word>>32 - n)

# Fonction : addition mod 2^32 des entiers qui correspondent aux mot de 32 bits. 
def add(A,B):
	return (A + B) % N


def sha1Hash(stringArray):
    
    # on souhaite savoir le nombre de bit que contient le mot, chaque caractere etant sur 8 bits
	l = len(stringArray)*8

	# Ajout d'un bit a 1 a la fin du message 
	stringArray.append(0x80);
    
	# calculs du nombre de zero a rajouter de facon a ce que le message soit divisible par 512 bits 
	nZeros = ( 448 - (len(stringArray))*8) % 0x200
	boxes = int(floor(nZeros/8));


	print ("Rajout de %i zeros en (boxes=%i) blocs") % (nZeros,boxes)

    # ici on ajoute les zero calculer precedement.
	for i in range(boxes): stringArray.append(0);

	# On verifie que la taille est < 2^32
	stringArray.append(0)
	stringArray.append(0)
	stringArray.append(0)
	stringArray.append(0)

	stringArray.append(0)
	stringArray.append(0)
	stringArray.append(0)
	stringArray.append(l)

	n = len(stringArray)/ 64


# initialisation 
	h0 = 0x67452301
	h1 = 0xEFCDAB89
	h2 = 0x98BADCFE
	h3 = 0x10325476
	h4 = 0xC3D2E1F0

	for i in range(n):

		startOfChunk = i*64
		w = [0]*80

		# Diviser le mot en 16
		for i in range(16):

			val = 0;

			for x in range(4):
				cell = stringArray[startOfChunk + 4*i + x]
				val = val << 8
				val |=cell

			w[i] = val

		for t in range(16,80):
			w[t] = leftRotate((w[t-3] ^ w[t-8] ^ w[t-14] ^ w[t-16]),1)

		A = h0
		B = h1
		C = h2
		D = h3
		E = h4

        # on applique les 80 rotations, en appliquant des constantes differentes celon t.
		for t in range(80):

			if t < 20:
				K = 0x5a827999
				f = (B & C) | ((B ^ 0xFFFFFFFF) & D)
			elif t < 40:
				K = 0x6ed9eba1
				f = B ^ C ^ D
			elif t < 60:
				K = 0x8f1bbcdc
				f = (B & C) | (B & D) | (C & D)
			else:
				K = 0xca62c1d6
				f = B ^ C ^ D

			temp = (leftRotate(A,5) + f + E + w[t] + K) & 0xFFFFFFFF;

			E = D
			D = C
			C = leftRotate(B,30)
			B = A
			A = temp 


		h0 = add(h0,A)
		h1 = add(h1,B)
		h2 = add(h2,C)
		h3 = add(h3,D)
		h4 = add(h4,E)
        
        print "Usual :" , convert_lisible(h0),convert_lisible(h1),convert_lisible(h2),convert_lisible(h3),convert_lisible(h4)
    #    print "Hexadecimal :", hex(h0),hex(h1),hex(h2),hex(h3),hex(h4)	


def convert_lisible(h):
    return str(hex(h))[2:10]

def main():

	if(len(sys.argv) < 2):
		print "usage: sha1 <Text Message>"
	else: 
		stringMsg = sys.argv[1] 
		stringArray = []
        # on  remplace chaque caractere par son equivalent dans la table ASCII 
		for byte in array.array('B', stringMsg): stringArray.append(byte)
        # print stringArray		
        sha1Hash(stringArray)


main()
