#! /usr/bin/python
# -*- coding:utf8 -*-

"""
    Test de performance des différents algorithmes de parenthésage:
    prend les fichiers test*.txt, de 5 à 20
"""

from matrices import *
import sys
from time import time
from numpy import matlib

path_perf = "tests/"


def main():

    if len(sys.argv) != 2:
        print "utilisation: test_performance <nom_fichier>"
        sys.exit(1)

    with open(sys.argv[1], "w") as fichier:
        for i in range(5, 21):
            print "Traitement du fichier perf"+str(i)+".txt"
            fichier.write(str(i)+"\t")
            n, dim, matrices = lireFichierMatrice(path_perf+"perf"+str(i)+".txt")

            debut = time()
            frontieres = matlib.zeros((n+1, n+1), dtype=int)
            resultat = trouverParenthesageOptimalNaif(dim, frontieres, 1, n)
            totalTemps = time() - debut
            fichier.write(str(totalTemps)+"\t")

            debut = time()
            frontieres.fill(0)
            resultat = trouverParenthesageOptimalAvecStockage(dim, frontieres, 1, n)
            totalTemps = time() - debut
            fichier.write(str(totalTemps)+"\t")

            debut = time()
            frontieres.fill(0)
            resultat = trouverParenthesageOptimalDynamique(n, dim, frontieres)
            totalTemps = time() - debut
            fichier.write(str(totalTemps)+"\n")



if __name__ == "__main__":
    main()
