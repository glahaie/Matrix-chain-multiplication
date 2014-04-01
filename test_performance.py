#! /usr/bin/python
# -*- coding:utf8 -*-

"""
    test_performance.py
    Par: Guillaume Lahaie

    Test de performance des différents algorithmes de parenthésage:
    genere une chaine de matrices aleatoire, et ensuite cherche
    le parenthésage optimal avec chaque algorithme. Si l'algorithme
    prend plus de 5 secondes, il est arrêté. Cela fonctionne
    seulement sur un système UNIX.
"""

from matrices import *
import sys
from time import time
from numpy import matlib
import random
from timeout import *

def main():

    if len(sys.argv) != 2:
        print "utilisation: test_performance <nombre>"
        sys.exit(1)

    matrices_max = int(sys.argv[1])
    for i in range(5, matrices_max+1):
        print "Temps d'exécution des algorithmes pour une chaine de "+ str(i) + " matrices"

        dim = random.sample(range(1, 1000), i+1)

        frontieres = matlib.zeros((i, i), dtype=int)
        with timeout(seconds=5):
            try:
                debut = time()
                resultat = trouverParenthesageOptimalNaif(dim, frontieres, 1, i)
                totalTemps = time() - debut
                print "Algorithme naif: \t\t\t" + str(totalTemps)
            except TimeoutError:
                print "Algorithme naif: \t\t\tplus de 5 secondes"

        debut = time()
        frontieres.fill(0)
        resultat = trouverParenthesageOptimalAvecStockage(dim, frontieres, 1,i)
        totalTemps = time() - debut
        print "Algorithme naif avec stockage: \t\t" + str(totalTemps)

        debut = time()
        frontieres.fill(0)
        resultat = trouverParenthesageOptimalDynamique(i, dim, frontieres)
        totalTemps = time() - debut
        print "Algorithme de programmation dynamique: \t" + str(totalTemps)
        print "-----------------------------------------------------------"



if __name__ == "__main__":
    main()
