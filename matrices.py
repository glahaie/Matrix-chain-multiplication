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
from time import time


###############################################################################
# Multiplication de deux matrices
###############################################################################

def multiplierMatrice(a, b):
    """Multiplie les matrices a et b, et retourne
       le résultat dans une nouvelle matrice"""

    #Vérifie si on peut bien multiplier les matrices
    dimA = a.shape
    dimB = b.shape

    #On multiplie -- vérifier le type de données
    c = matlib.empty((dimA[0], dimB[1]))
    for i in range(0, dimA[0]):
        for j in range(0, dimB[1]):
            total = 0
            for k in range(0, dimA[1]):
                total += a[i,k] * b[k,j]
            c[i,j] = total
    return c

###############################################################################
# Algorithme 1: Approche diviser pour régner sans stockage de résultat
###############################################################################
def trouverParenthesageOptimalNaif(dim, frontiere, i, j):
    """Calcule récursivement le meilleure parenthésage pour une
       série de multiplications de matrices. Il effectue le calcul
       de façon récursive
       frontiere: matrice de position des parenthèses pour deux matrices
       dim: tableau de dimensions des matrices à multiplier
    """
    minimum = 0
    if i != j:
        minimum = sys.maxint    #minimum = infini
        for k in range(i, j):
            gauche = trouverParenthesageOptimalNaif(dim, frontiere, i, k)
            droite = trouverParenthesageOptimalNaif(dim, frontiere, k+1, j)
            total = gauche + droite + dim[i-1]*dim[k]*dim[j]
            if total < minimum:
                frontiereTemp = k
                minimum = total
        frontiere[i, j] = frontiereTemp
    return minimum

###############################################################################
# Algorithme 2: Approche diviser pour régner avec stockage de résultat
###############################################################################
def trouverParenthesageOptimalAvecStockage(dim, frontiere, i, j):
    """Calcule récursivement le meilleure parenthésage pour une
       série de multiplications de matrices. Il effectue le calcul
       de façon récursive
       frontiere: matrice de position des parentheses pour deux matrices
       dim: tableau de dimensions des matrices à multiplier
       m: résultats déjà calculés
    """
    m = matlib.empty((len(dim), len(dim)), dtype=int)
    m.fill(-1)
    return __trouverParenthesageOptimalAvecStockage(frontiere, dim, m, i, j)

def __trouverParenthesageOptimalAvecStockage(frontiere, dim, m, i, j):
    minimum = 0
    if i != j:
        minimum = sys.maxint
        for k in range(i, j):
            if(m[i,k] < 0):
                m[i, k] = __trouverParenthesageOptimalAvecStockage(frontiere, dim, m, i, k)
            if(m[k+1,j] < 0):
                m[k+1,j] = __trouverParenthesageOptimalAvecStockage(frontiere, dim, m, k+1, j)
            total = m[i,k] + m[k+1,j] + dim[i-1]*dim[k]*dim[j]
            if total < minimum:
                frontiereTemp = k
                minimum = total
        frontiere[i, j] = frontiereTemp
    return minimum

###############################################################################
# Algorithme 3: Programmation dynamique
###############################################################################
def trouverParenthesageOptimalDynamique(n, dim, frontiere):
    """Parenthésage optimal selon l'algorithme de programmation dynamique
       retourne m, la matrice de cout minimal pour toutes les chaines de
       multiplication.

       Pour obtenir le résultat de toute la chaine de multiplication, il
       faut regarder à m[1, n]
    """
    m = matlib.zeros((n+1, n+1), dtype=int)
    for i in range(1, n+1):
        m[i,i] = 0
    for l in range(2, n+1):
        for i in range(1, n-l+2):
            j = i + l -1
            m[i,j] = sys.maxint
            for k in range(i, j):
                q = m[i,k] + m[k+1, j] + dim[i-1]*dim[k]*dim[j]
                if q < m[i,j]:
                    m[i,j] = q
                    frontiere[i,j] = k
    return m


###############################################################################
# Affiche le parenthésage optimal des matrices
###############################################################################
def afficherParenthesageOptimal(frontieres, i, j):
    __afficherParenthesageOptimal(frontieres, i, j)
    print

def __afficherParenthesageOptimal(frontieres, i, j):
    """Affiche le parenthésage optimal pour un chaine de matrices selon
    les résultats compris dans la matrice frontieres. Source: Introduction
    to Algorithms, 3rd edition
    """
    if i == j:
        sys.stdout.write("A"+str(i))
    else:
        sys.stdout.write("(")
        __afficherParenthesageOptimal(frontieres, i, frontieres[i, j])
        __afficherParenthesageOptimal(frontieres, frontieres[i, j]+1, j)
        sys.stdout.write(")")


def calculerParentheses(frontieres, info, i, j):
    #On regarde les parenthèse pour le moment
    if i != j:
        k = frontieres[i,j]
        if i != k:
            info[i]["avant"] += 1
            info[k]["apres"] += 1
            calculerParentheses(frontieres, info, i, k)
        if k+1 != j:
            info[k+1]["avant"] += 1
            info[j]["apres"] += 1
            calculerParentheses(frontieres, info, k+1,j)

###############################################################################
# Multiplication en chaine de matrices de facon optimal selon frontiere
###############################################################################
def multiplierChaineMatrice(frontieres, matrices, i, j):
    """
        Multiplication des matrices de la liste matrices de façon optimale,
        à partir des informations de la matrice frontieres
    """
    if i < j:
        c = multiplierChaineMatrice(frontieres, matrices, i, frontieres[i,j])
        d = multiplierChaineMatrice(frontieres, matrices, frontieres[i,j]+1, j)
        return multiplierMatrice(c,d)
    else:
        return matrices[i]

###############################################################################
# Lecture du fichier et initialisation des matrices
###############################################################################
def lireFichierMatrice(fichier):
    with open(fichier, "r") as fichier:
        noMatrice = int(fichier.readline())
        dimensions = map(int,
                         filter(lambda x: x != "",
                                map(lambda x: x.strip(),
                                    fichier.readline().strip().split(" "))))

        assert (len(dimensions) == noMatrice+1),"Erreur de dimensions dans le fichier"

        matrices = [None]
        for i in range(0, len(dimensions)-1):
                matrice = []
                # On remplit la matrice
                for j in range(0, dimensions[i]):
                    temp = map(int,
                            filter(lambda x: x != "",
                                map(lambda x: x.strip(),
                                    fichier.readline().strip().split(" ")
                                    )
                                )
                            )
                    if len(temp) != dimensions[i+1]:
                        print "Erreur dans le fichier source"
                        sys.exit(1)
                    matrice.append(temp)
                matrices.append(matlib.matrix(matrice))
    return noMatrice, dimensions, matrices

def main():
    """Comportement si on exécute le programme directement:
        on lit le fichier matrices.txt pour obtenir l'information
        sur les matrices, on exécute ensuite la recherche du
        parenthésage optimal, et on écrit dans resultat.txt les
        matrices frontieres, m, et ensuite le résultat de la multiplication"""

    #On lit le fichier
    n, dimensions, matrices = lireFichierMatrice("matrices.txt")

    with open("resultat.txt", "w") as resultat:
        frontieres = matlib.zeros((n+1, n+1), dtype=int)
        m = trouverParenthesageOptimalDynamique(n, dimensions, frontieres)
        for line in m.tolist():
            resultat.write(reduce(lambda x, y: x+y,
                                  map(lambda x: str(x)+" ", line)))
            resultat.write("\n")
        for line in frontieres.tolist():
            resultat.write(reduce(lambda x, y: x+y,
                                  map(lambda x: str(x)+" ", line)))
            resultat.write("\n")
        resultat.write(str(m[1,n])+"\n")



if __name__ == "__main__":
    main()

