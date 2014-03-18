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


class ParNaif:
    """Algorithme de parenthésage naif, diviser pour régner,
       sans stockage des résultats déjà calculés"""

    def __init__(self, dimensions):
        self.dim = dimensions
        #La matrice est trop grande pour le moment, pour faciliter l'accès
        self.frontieres = matlib.zeros((len(self.dim), len(self.dim)), dtype=int)

    def trouverParenthesageOptimal(self):
        return self.__trouverParenthesageOptimal(1, len(self.dim)-1)

    def __trouverParenthesageOptimal(self, i, j):
        """Calcule récursivement le meilleure parenthésage pour une
           série de multiplications de matrices. Il effectue le calcul
           de façon récursive
        """
        minimum = 0
        if i != j:
            minimum = sys.maxint    #minimum = infini
            for k in range(i, j):
                gauche = self.__trouverParenthesageOptimal(i, k)
                droite = self.__trouverParenthesageOptimal(k+1, j)
                total = gauche + droite + self.dim[i-1]*self.dim[k]*self.dim[j]
                if total < minimum:
                    frontiereTemp = k
                    minimum = total
            self.frontieres[i, j] = frontiereTemp
        return minimum
    
    #Afficher le parenthésage optimal de la matrice frontières
    def afficherParenthesageOptimal(self):
        self.info = {}
        debut = ord('A')
        for i in range(0, len(self.dim)-1):
            nom = chr(debut+i)
            parAvant = 0
            parApres = 0
            self.info[i+1] = {"nom":nom, "avant":parAvant, "apres":parApres}
        
        self.__calculerParentheses(1, len(self.dim)-1)

        #On affiche
        for i in range(1, len(self.dim)):
            for j in range(0, self.info[i]["avant"]):
                sys.stdout.write("(")
            sys.stdout.write(self.info[i]["nom"])
            for j in range(0, self.info[i]["apres"]):
                sys.stdout.write(")")
        sys.stdout.write("\n")


    def __calculerParentheses(self, i, j):
        #On regarde les parenthèse pour le moment
        if i != j:
            k = self.frontieres[i,j]
            if i != k:
                self.info[i]["avant"] += 1
                self.info[k]["apres"] += 1
                self.__calculerParentheses(i, k)
            if k+1 != j:
                self.info[k+1]["avant"] += 1
                self.info[j]["apres"] += 1
                self.__calculerParentheses(k+1,j)





class ParNaifAvecMemoire:
    """Algorithme de parenthésage naif, diviser pour régner,
       On stocke les résultats intermédiaires, et on les calcules seulement si nécessaire"""

    def __init__(self, dimensions):
        self.dim = dimensions
        #La matrice est trop grande pour le moment, pour faciliter l'accès
        self.frontieres = matlib.zeros((len(self.dim), len(self.dim)), dtype=int)
        self.m = matlib.empty((len(self.dim), len(self.dim)), dtype=int)
        self.m.fill(-1)

    def trouverParenthesageOptimal(self):
        self.m[1,len(self.dim)-1] = self.__trouverParenthesageOptimal(1, len(self.dim)-1)
        return self.m[1, len(self.dim)-1]

    def __trouverParenthesageOptimal(self, i, j):
        """Calcule récursivement le meilleure parenthésage pour une
           série de multiplications de matrices. Il effectue le calcul
           de façon récursive
        """
        minimum = 0
        if i != j:
            minimum = sys.maxint    #minimum = infini
            for k in range(i, j):
                if(self.m[i,k] < 0):
                    self.m[i, k] =self.__trouverParenthesageOptimal(i, k)
                if(self.m[k+1,j] < 0):
                    self.m[k+1,j] = self.__trouverParenthesageOptimal(k+1, j)
                total = self.m[i,k] + self.m[k+1,j] + self.dim[i-1]*self.dim[k]*self.dim[j]
                if total < minimum:
                    frontiereTemp = k
                    minimum = total
            self.frontieres[i, j] = frontiereTemp
        return minimum


class AlgoDynamique:
    """Implémentation de l'algorithme en programmation dynamique pour
       le parenthésage"""
    def __init__(self, dimensions):
        self.dim = dimensions
        self.frontieres = matlib.zeros((len(self.dim), len(self.dim)), dtype=int)
        self.m = matlib.zeros((len(self.dim), len(self.dim)), dtype=int)

    def trouverParenthesageOptimal(self):
        self.calculerM()
        return self.m[1,len(self.dim)-1]

    def calculerM(self):
        """On remplit la matrice m des résultats partiels"""
        n = len(self.dim)
        for i in range(1, n):
            self.m[i,i] = 0
        for l in range(2, n):
            for i in range(1, n-l+1):
                j = i + l -1
                self.m[i,j] = sys.maxint
                for k in range(i, j):
                    q = self.m[i,k] + self.m[k+1, j] + self.dim[i-1]*self.dim[k]*self.dim[j]
                    if q < self.m[i,j]:
                        self.m[i,j] = q
                        self.frontieres[i,j] = k

#Multiplie les matrices de la liste matrices, de façon optimal, à l'aide
#du résultat de frontières
def multiplierChaineMatrice(frontieres, matrices, i, j):
    if i < j:
        c = multiplierChaineMatrice(frontieres, matrices, i, frontieres[i,j])
        d = multiplierChaineMatrice(frontieres, matrices, frontieres[i,j]+1, j)
        return multiplierMatrice(c,d)
    else:
        return matrices[i]



def main():
    a = matlib.ones((2, 3))
    b = matlib.ones((3, 2))
    print(a)
    print(b)
    
    c = multiplierMatrice(a, b)

    print(c)

    dimensions = [13, 5, 89, 3, 34]

    matrices = [matlib.zeros((1, 1),dtype=int)]
    for i in range(0, len(dimensions)-1):
        matrice = matlib.zeros((dimensions[i], dimensions[i+1]), dtype=int)

        for j in range(0, min(dimensions[i], dimensions[i+1])):
                matrice[j,j] = 1
        print matrice
        matrices.append(matrice)
 
    #Algo naif, #1
    naif = ParNaif(dimensions)
    resultat = naif.trouverParenthesageOptimal()

    print "resultat = " + str(resultat)
    print naif.frontieres
    naif.afficherParenthesageOptimal()

#    #Algo naif, #2: avec mémoire
    #memoire = ParNaifAvecMemoire(dimensions)
    #resultat = memoire.trouverParenthesageOptimal()

    #print "resultat = " + str(resultat)
    #print memoire.frontieres
    #print memoire.m

    ##Algo 3: prog dynamique
    #dynamique = AlgoDynamique(dimensions)
    #resultat = dynamique.trouverParenthesageOptimal()

    #print "resultat = " + str(resultat)
    #print dynamique.frontieres
    #print dynamique.m



if __name__ == "__main__":
    main()

