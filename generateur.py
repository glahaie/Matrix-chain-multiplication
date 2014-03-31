#! /usr/bin/python
# -*- coding:utf8 -*-

"""
generateur.py
Par Guillaume Lahaie
LAHG04077707

Génère des matrices de grandeur aléatoire avec des valeurs
de -1 à 1, en entier, selon le nombre donné en entré, enregistré
dans le fichier nommé en argument 2
"""

import sys
import os
import random


def genererMatrices(n, nom_fichier):
    """Crée de façon aléatoire n matrices, de dimensions
       permettant de faire une multiplication en chaine, et
       enregistre les résultats dans nom_fichier
    """
    with open(nom_fichier, "w") as fichier:
        #Nombre de matrices
        fichier.write(str(n)+"\n")
        #On génére les dimensions, entre 3 et 300
        dimensions = random.sample(range(3, 300), n+1)
        fichier.write(reduce(lambda x, y: x + y,
                                 map(lambda x: str(x)+" ", dimensions),
                                 ""
                                 ) + "\n"
                          )
        #On génère les matrices
        for i in range(0, n):
            genererMatrice(fichier, dimensions[i], dimensions[i+1])

def genererMatrice(fichier, i, j):
    for k in range(0, i):
        for l in range(0, j):
            fichier.write(str(random.randint(-1, 1)) + " ")
        fichier.write("\n")

def main():
    print sys.argv
    if len(sys.argv) != 3:
        print "Utilisation: generateur.py <no matrices> <no_fichier>"
        sys.exit(1)
    nombreMat = int(sys.argv[1])
    if nombreMat <= 0:
        print "Vous devez entrer un nombre de matrices plus grand ou égal à 1"
        sys.exit(1)
    if os.path.isfile(sys.argv[2]):
        while True:
            print "Le fichier " + sys.argv[2] + " existe, voulez-vous l'écraser? (o/n)"
            reponse = raw_input().strip().lower()
            if reponse == 'o':
                break
            elif reponse == "n":
                print "Programme arrêté"
                sys.exit(1)
            else:
                print "Réponse invalide, entrer (o/n)"
    genererMatrices(nombreMat, sys.argv[2])



if __name__ == "__main__":
    main()
