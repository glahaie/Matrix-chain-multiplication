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
def trouverParenthesageOptimalNaif(frontiere, dim, i, j):
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
            gauche = trouverParenthesageOptimalNaif(frontiere, dim, i, k)
            droite = trouverParenthesageOptimalNaif(frontiere, dim, k+1, j)
            total = gauche + droite + dim[i-1]*dim[k]*dim[j]
            if total < minimum:
                frontiereTemp = k
                minimum = total
        frontiere[i, j] = frontiereTemp
    return minimum

###############################################################################
# Algorithme 2: Approche diviser pour régner avec stockage de résultat
###############################################################################
def trouverParenthesageOptimalAvecStockage(frontiere, dim):
    """Calcule récursivement le meilleure parenthésage pour une
       série de multiplications de matrices. Il effectue le calcul
       de façon récursive
       frontiere: matrice de position des parentheses pour deux matrices
       dim: tableau de dimensions des matrices à multiplier
       m: résultats déjà calculés
    """
    m = matlib.empty((len(dim), len(dim)), dtype=int)
    m.fill(-1)
    return __trouverParenthesageOptimalAvecStockage(frontiere, dim, m, 1, len(dim)-1)

def __trouverParenthesageOptimalAvecStockage(frontiere, dim, m, i, j):
    minimum = 0
    if i != j:
        minimum = sys.maxint    #minimum = infini
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
def trouverParenthesageOptimalDynamique(frontiere, dim):
    """On remplit la matrice m des résultats partiels"""
    m = matlib.zeros((len(dim), len(dim)), dtype=int)
    n = len(dim)
    for i in range(1, n):
        m[i,i] = 0
    for l in range(2, n):
        for i in range(1, n-l+1):
            j = i + l -1
            m[i,j] = sys.maxint
            for k in range(i, j):
                q = m[i,k] + m[k+1, j] + dim[i-1]*dim[k]*dim[j]
                if q < m[i,j]:
                    m[i,j] = q
                    frontiere[i,j] = k
    return m[1, len(dim) -1]


###############################################################################
# Affiche le parenthésage optimal des matrices
###############################################################################
def afficherParenthesageOptimal(frontieres):
    """Affiche le parenthésage optimal pour un chaine de matrices selon
       les résultats compris dans la matrice frontieres
    """
    info = {}
    for i in range(1, frontieres.shape[0]):
        nom = "A" + str(i)
        parAvant = 0
        parApres = 0
        info[i] = {"nom":nom, "avant":parAvant, "apres":parApres}
    
    calculerParentheses(frontieres, info, 1, frontieres.shape[0]-1)

    #On affiche
    for i in range(1, frontieres.shape[1]):
        sys.stdout.write( "("*info[i]["avant"] + info[i]["nom"] + ")"*info[i]["apres"])
    print


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
    with open(fichier, "r") as matrices:
        noMatrice = int(matrices.readline())
        dimensions = map(int, matrices.readline().strip().split(" "))
        print noMatrice
        print dimensions


def main():
    if len(sys.argv) != 2:
        print "Utilisation: matrice.py <nom_fichier>"
        sys.exit(1)

    dimensions = [13, 5, 89, 3, 34]

    matrices = [matlib.zeros((1, 1),dtype=int)]
    for i in range(0, len(dimensions)-1):
        matrice = matlib.zeros((dimensions[i], dimensions[i+1]), dtype=int)

        for j in range(0, min(dimensions[i], dimensions[i+1])):
                matrice[j,j] = 1
        matrices.append(matrice)
 
#    #Algo naif, #1
    #frontieres = matlib.zeros((len(dimensions), len(dimensions)), dtype=int)
    #resultat = trouverParenthesageOptimalNaif(frontieres, dimensions,1, len(dimensions)-1)

    #print "resultat = " + str(resultat)
    #print frontieres
    #afficherParenthesageOptimal(frontieres)

#    #algo #2, avec stockage de mémoire
    #frontieres = matlib.zeros((len(dimensions), len(dimensions)), dtype=int)
    #resultat = trouverParenthesageOptimalAvecStockage(frontieres, dimensions)

    #print "resultat = " + str(resultat)
    #print frontieres
    #afficherParenthesageOptimal(frontieres)

    #algo #3, programmation dynamique
    frontieres = matlib.zeros((len(dimensions), len(dimensions)), dtype=int)
    resultat = trouverParenthesageOptimalDynamique(frontieres, dimensions)

    print "resultat = " + str(resultat)
    print frontieres
    afficherParenthesageOptimal(frontieres)

    #dynamique = AlgoDynamique(dimensions)
    #resultat = dynamique.trouverParenthesageOptimal()

    #print "resultat = " + str(resultat)
    #print dynamique.frontieres
    #print dynamique.m
    lireFichierMatrice(sys.argv[1])



if __name__ == "__main__":
    main()

