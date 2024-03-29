Matrix chain multiplication
=======

Implementation of different algorithms to solve the
[Matrix chain multiplication problem](http://en.wikipedia.org/wiki/Matrix_chain_multiplication).

Three algorithms are implemented: a naive, divide-to-conquer algorithm,
a divide-to-conquer algorithm that saves results already calculated and
a dynamic programming algorithm.

The goal is to compare the time to obtain the result with the algorithms.
Since the time for the naive algorithms grows exponentially, I use signals
to stop the calcultation if it takes more than 5 seconds. This will not
work on Windows.

***

Algorithme de parenthésage optimal
=======

Implémentation en python des algorithmes de calcul
de parenthésage optimal:

* Algorithme diviser pour régner
* Algorithme diviser pour régner avec stockage
* Algorithme en programmation dynamique

Par défaut, le fichier matrices.py lit un fichier matrices.txt et
enregistre le résultat obtenu avec l'algorithme de programmation
dynamique. Il est possible d'importer matrices.py pour utiliser
les autres algorithmes.

Le fichier test_matrices.py contient des tests unitaires vérifiant
les résultats des fonctions de multiplication de matrices,
l'exactitude des résultats pour les 3 algorithmes, et l'affichage
du parenthésage.

Pour tester la vitesse d'exécution des algorithmes, il faut utiliser
le fichier test_performance.py, en entrant le nombre maximal de
matrices dans la chaine. à ce moment, le programme affiche à
l'écran les temps d'exécution pour les trois algorithmes. L'algorithme
naif n'est plus considéré lorsque n > 20.


* Pour tester le résultat obtenu à partir du fichier matrices.txt:
  * python matrices.py

* Pour vérifier les tests unitaires:
  * python test_matrices.py

* Pour tester la performance des algorithmes de x = 5 à n matrices:
  * python test_performance.py nombre
