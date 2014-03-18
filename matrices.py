#! /usr/bin/python
# -*- coding:utf8 -*-

"""matrices.py
   Par Guillaume Lahaie
   dernière modification: 17 mars 2014

   Implémentation des algorithmes de parenthésage vu en cours.
   Tout d'abord, l'algorithme diviser pour régner, et ensuite
   l'algorithme de programmation dynamique
"""

from numpy import matlib
import sys


def multiplication(a, b):
    """Multiplie les matrices a et b, et retourne
       le résultat dans une nouvelle matrice"""

    #Vérifie si on peut bien multiplier les matrices
    dimA = a.shape
    dimB = b.shape

    if dimA[1] != dimB[0]:
#erreur
        print "ERREUR"
        return None
    else:
        #On multiplie -- vérifier le type de données
        c = matlib.empty((dimA[0], dimB[1]))
        for i in range(0, dimA[0]):
            for j in range(0, dimB[1]):
                total = 0
                for k in range(0, dimA[1]):
                    total += a[i,k] * b[k,j]
                c[i,j] = total
        return c

#nbMatrices: le nombre de matrices à multiplier
#dimensions: les dimensions des matrices
#out: le nombre de multiplications et la matrice frontieres
def parenthesage_naif(nbMatrices, dimensions):
    """Calcule récursivement le meilleure parenthésage pour une
       série de multiplications de matrices. Il effectue le calcul
       de façon récursive"""
    
    f = matlib.zeros()
    nbMult, frontieres = trouverParenthesageRecursif(0, nbMatrices, dimensions, f)
    return nbMult, frontieres


def trouverParenthesageRecursif(i, j, dim, frontiere):
    """Appel récursif pour trouver le meilleur parenthésage"""
    minimum = 0
    if i != j:
        minimum = sys.maxint
        for k in range(i, j):
            gauche, frontiere = trouverParenthesageRecursif(i, k,dim, frontiere)
            droite, frontiere = trouverParenthesageRecursif(k+1, j, dim, frontiere)
            total = gauche + droite + dim[i-1]*dim[k]*dim[j]
            if total < minimum:
                minimum = total
                frontiereTemp = k
        frontiere[i,j] = frontiereTemp
    return minimum, frontiere

def main():
    a = matlib.ones((2, 3))
    b = matlib.ones((3, 2))
    print(a)
    print(b)
    
    c = multiplication(a, b)

    print(c)



    #On test le premier parenthesage
    

if __name__ == "__main__":
    main()

