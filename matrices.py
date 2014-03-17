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


def main():
    a = matlib.ones((2, 3))
    b = matlib.ones((3, 2))
    print(a)
    print(b)
    
    c = multiplication(a, b)

    print(c)


if __name__ == "__main__":
    main()

