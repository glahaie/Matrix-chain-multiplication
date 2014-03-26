#! /usr/bin/python
# -*- coding:utf8 -*-

"""
    test_matrices.py
    Teste les fonctions de de matrices.py
"""

from matrices import *
import unittest
from numpy import matlib
import numpy
from StringIO import StringIO
import sys

class TestMultiplicationSimple(unittest.TestCase):

    def test_mult_simple(self):
        tempa = [[1,0,0],[0,1,0],[0,0,1]]
        self.a = matlib.matrix(tempa)
        self.b = matlib.matrix(tempa)
        self.c = matlib.matrix(tempa)
        self.d = multiplierMatrice(self.a, self.b)
        self.assertTrue(numpy.array_equal(self.c, self.d))

    def test_mult_dimensions(self):
        tempa = [[1,1],[2,2],[3,3]]
        tempb = [[3,3,3],[2,2,2]]
        tempc = [[5,5,5],[10,10,10],[15, 15, 15]]
        self.a = matlib.matrix(tempa)
        self.b = matlib.matrix(tempb)
        self.c = matlib.matrix(tempc)
        self.assertTrue(numpy.array_equal(multiplierMatrice(self.a, self.b), self.c))

class TestAlgoNaif(unittest.TestCase):

    def test_resultat_notes(self):
        self.dim = [13, 5, 89, 3, 34]
        self.frontieres = matlib.zeros((4, 4), dtype=int)
        result = [[0, 1, 1, 3],
                  [0, 0, 2, 3],
                  [0, 0, 0, 3],
                  [0, 0, 0, 0]]
        self.frontiereResult = matlib.matrix(result)
        self.assertEqual(2856, trouverParenthesageOptimalNaif(self.dim,
                                                         self.frontieres, 1, 4))
        self.assertTrue(numpy.array_equal(self.frontieres, self.frontiereResult))

class TestAlgoStockage(unittest.TestCase):

    def test_resultat_notes(self):
        self.dim = [13, 5, 89, 3, 34]
        self.frontieres = matlib.zeros((4, 4), dtype=int)
        result = [[0, 1, 1, 3],
                  [0, 0, 2, 3],
                  [0, 0, 0, 3],
                  [0, 0, 0, 0]]
        self.frontiereResult = matlib.matrix(result)
        self.assertEqual(2856, trouverParenthesageOptimalAvecStockage(self.dim,
                                                         self.frontieres, 1, 4))
        self.assertTrue(numpy.array_equal(self.frontieres, self.frontiereResult))

class TestAlgoDynamique(unittest.TestCase):

    def test_resultat_notes(self):
        self.dim = [13, 5, 89, 3, 34]
        self.frontieres = matlib.zeros((5, 5), dtype=int)
        result = [[0, 0, 0, 0, 0],
                  [0, 0, 1, 1, 3],
                  [0, 0, 0, 2, 3],
                  [0, 0, 0, 0, 3],
                  [0, 0, 0, 0, 0]]
        self.frontiereResult = matlib.matrix(result)
        self.m = trouverParenthesageOptimalDynamique(4, self.dim,
                                                         self.frontieres)
        self.assertEqual(2856, self.m[1, 4])
        self.assertTrue(numpy.array_equal(self.frontieres, self.frontiereResult))

class TestAffichageParenthesage(unittest.TestCase):

    def test_affichage(self):
        save_stdout = sys.stdout
        out = StringIO()
        sys.stdout = out
        frontieres = [[0, 1, 1, 3],
                  [0, 0, 2, 3],
                  [0, 0, 0, 3],
                  [0, 0, 0, 0]]
        self.frontieres = matlib.matrix(frontieres)
        afficherParenthesageOptimal(self.frontieres, 1, 4)
        output = out.getvalue().strip()
        self.assertEquals("((A1(A2A3))A4)",output)
        sys.stdout = save_stdout


if __name__ == "__main__":
    unittest.main()
