BELLEC Gwendal
PIERSON Louis


Création d'une IA jouant au Go :

Dans ce fichier ci-dessous nous allons vous présenter en détail les méthodes que nous avons utliser pour créer notre IA, faire en sorte qu'elle
ait de bonnes prédictions et qu'elle ait une bonne complexité spatiale et surtout temporelle.


Implémentation de l'algo-alpha :
Tout d'abord nous avons implémenté un algorithme alpha-beta pour effectuer notre recherche de noeud optimal dans notre arbre de jeu.
Il s'agit simplement d'une fontion récursive qui fait remonter le noeud optimal et son heuristique depuis la profondeur maximale prédéfinie ou
depuis une fin de partie.


Implémentation de l'heuristique maison:
Notre heuristique maison évalue un plateau de jeu par rapport à la différence de scores des deux joueurs, le but étant de trouver les plateaux où
l'on augmente notre propre score ou les plateaux où l'on empêche l'adversairr d'augmenter son propre score.


Amélioration de l'heuristique en diminuant l'heuristique des cases aux extrémités
Cette heuristique permettait déjà de prendre les pions de l'adversaire si possible et de l'empêcher de nous prendre des pions. Cependant dans les cas où
le score ne bouge peu importe on nous jouons et on l'adveraire joue, il peut être intéressant d'effctuer ou d'éviter de faire certains coups.
Ainsi, les coups joués en bordure de plateau feront dimininuer notre heuristique lorsque que c'est nous qui le jouer et fetont augmenter notre heuristique
lorsque que c'est l'adveraire qui le jouera. Donc à part en cas de tentative d'une prise d'un ou plusieurs pions ou en cas de défense d'un ou plusieurs
pions. Enfin, la manière avec laquelle nous avons créé implémenter notre heuristique fait que notre IA jouera toujours (à part en cas de prise ou de
défense de pions) à proximité d'un de ses pions ce qui a pour conséquence de générer un motif dès le début de partie voir des motifs en fin de partie.


Gestion des "PASS":
Jouer un "PASS" a été implémenté de manière différente de placer un pion sur case. Notre IA joue "PASS" dans seulement deux cas distincts, si l'adversaire
fait "PASS" et que nous avons plus de points que lui, dans ce cas nous jouous aussi "PASS" et si nous ne pouvons que jouer "PASS" nous jouons "PASS".


Gestion du temps maximal imparti:
Comme indiqué dans le sujet, notre IA posséde un temps de calcul réel de 30min par partie. Ainsi si jamais nous dépassons un temps de calcul supérieur
à 25min, nous limitons la profondeur de recherche dans l'algorithme alpha-beta à 2. Ce critère est très empirique, on part du principe que la puissance de
calcul qui nous sera fourni sera très inférieur à celle dont nous disposons avec nos ordinateurs. Or avec une profondeur de 2 notre algorithme met quelques
minutes à effectuer une partie, sachant que plus la partie avance, plus notre algorithme trouve un coup à jouer rapidement.
On suppose qu'avec 25 minutes de partie déjà écoulées, 5min seront suffisante pour trouver les derrière coup qui ne seront à priori pas très couteux
à trouver.


Profondeur maximale variable:
Enfin nous avons implémenter une fonction choisissant notre profondeur maximale de recherche des coups avec l'algorithme alpha-beta. Ici aussi, la
profondeur maximale de recherche est trouvée selon des critères très empirique. Nous partons du principe que la recherche d'un coup ne doit pas excéder
la durée de recherche du premier coup pour une profondeur de 2. Or chercher un coup en début de partie pour un arbre de profondeur 2 correspond à parcourir
un arbre de taille 81*80 (car nous avons d'abord 81 coups possibles car il y a 81 cases de plateaux si l'on ne compte pas l'action "PASS"). Ainsi, plus la
partie avancera et plus le nombre de coups jouables sera petit et plus nombre pourront parcourir l'arbre profondément. Le critère étant que l'arbre à
parcourir ne doit pas avoir plus de 81*80 feuilles.


De quoi nous sommes le plus fier : la profondeur maximale variable
Ce dont nous sommes le plus fier dans notre implémentation est la profondeur de recherche variable car elle permet de garder une bonne complexité temporelle
en début et en fin de partie tout en ayant une IA qui pourra prédir plus de coup à l'avance en fin. Or prédir beaucoup de coup à l'avvance en fin de partie
est très important car si nous avons un score proche de celui de notre adversaire, il s'agit du moment où nous pouvons lui prendre beaucoup de pions s'il
joue mal ou il peut nous prendre beaucoup de pions si l'on joue mal.