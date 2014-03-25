set encoding utf8
set title "Temps d'exécution des algorithmes pour différentes chaines de matrices" 
set xlabel "Nombre de matrices dans la chaine"
set ylabel "Temps d'exécution (en secondes)"



set terminal postscript landscape color
set output "resultat2.eps"

plot 'resultat.txt' u 1:3 title 'Algorithme naif avec stockage' with linespoints, \
'resultat.txt' u 1:4 title 'Algorithme de programmation dynamique' with linespoints
