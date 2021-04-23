import os, subprocess, sys
from Fourmis import *
#
#Classe graphe représentant un graphe non orienté par ue matrice qui peut etre converti en .dot 
#
#Le noeud 0 correspond au noeud A dans le png, le 1 au B ect ...
#
#Ex d'une matrice valide :
#		-1	2	3	5
#
#		2	-1	4	2
#
#		3	4	-1	5	
#
#		5	2	5	-1
#
#Puisque le graphe est non orienté si il existe un liens de A vers B il existe aussi un liens de B vers A ayant le meme poids
#Un poids de -1 signifie que le liens est inexistant
#
class Graph :

	def __init__(self,matDistances):
		#On intitialise la matrice représentant les liens entre les noeuds
		self.matDistances = matDistances
		self.corrigerErreur()
		#On construit la même matrice renseignant la quantité de pheromone sur chaque lien
		#Parexemple self.matPheromones[0][1] renseigne sur la quantité de phéomone présente sur le chemin allant du noeud 0 au noeud 1
		#Par defaut la quantite de pheromone est a 0
		self.matPheromones = [ [1]*len(self.matDistances[0]) for i in range(len(self.matDistances))]
		for successeur in range(0,len(self.matDistances)):
			for predecesseur in range(0,len(self.matDistances[0])):
				if(successeur == predecesseur or self.matDistances[successeur][predecesseur] == -1 ):
					self.matPheromones[successeur][predecesseur] = -1

	#Verifie que la matrcie soit valide
	def matValide(self):
		#Si la matrice n'est pas de taille carré ( 2X2 , 3X3, 4X4) la matrice n'est pas valide
		for ligne in range(0,len(self.matDistances)):
			if(len(self.matDistances) != len(self.matDistances[ligne])):
				print("La matrice doit etre de taile carre \n")
				return False
		#Puisque le graphe est non orienté si il existe un lien de A vers B il existe aussi un lien de B vers A ayant le même poids
		for successeur in range(0,len(self.matDistances)):
			for predecesseur in range(0,len(self.matDistances[0])):
				if(self.matDistances[successeur][predecesseur] != self.matDistances[predecesseur][successeur]):
					print("Matrice non valide \n")
					return False
		print("Matrice valide \n")
		return True

	#Corrige les eventuelles erreurs dans la matrice
	def corrigerErreur(self):
		print("Correction des eventuelles erreurs")
		#Pour chaque lien
		for successeur in range(0,len(self.matDistances)):
			for predecesseur in range(0,len(self.matDistances[0])):
				#Puisque le graphe est non orienté si il existe un lien de A vers B, alors il existe aussi un liens de B vers A ayant le meme poids
				if(self.matDistances[successeur][predecesseur] != self.matDistances[predecesseur][successeur]):
					self.matDistances[predecesseur][successeur] = self.matDistances[successeur][predecesseur]
				#On met à -1 "les puits" (les liens d'un noeud vers lui meme) 
				if(successeur == predecesseur):
					self.matDistances[successeur][predecesseur] = -1


	#Algorithme de colonnies de fourmis retournant le plus court chemin
	#
	#debut : noeud de départ (valeur comprise entre 0 et dimMatrice -1)
	#debut : noeud d'arrivé (valeur comprise entre 0 et dimMatrice -1)
	#
	#nbFourmis : Nombre de fourmis
	#nbMouvementsParFourmi : chanque fourmis vont effectuer nbMouvementsParFourmi avant la fin de l'algorithme
	#
	#pho : evaporation de pho % par generation
	#
	#alpha controle la fonction de transition proportionelle plus alpha est grand plus la fourmis va se fiés au phéromone 
	#
	#beta controle la fonction de transition proportionelle plus beta est grand, plus la fourmis va avoir tendance à aller au prochain noeuds le plus proche (le noeuds avec la plus grande visibilité)
	#
	#Gamma controle la fonction de transition proportionelle plus gamma est grand, plus la fourmis à tendance à explorer des chemins inexplorés
	def shortestPathACO(self,debut,fin,nbFourmis,pho,alpha,beta,gamma,nbGeneration=50):
		if(debut == fin):
			return [debut]
		listFourmis = []
		#Creation des nbFourmis au point de départ
		for i in range(nbFourmis):
			listFourmis.append(Fourmis(debut))
		#Toutes les fourmis font nbGenerations aller-retour
		for i in range(0,nbGeneration):
			#Toutes les fourmis font un "aller-retour"
			for fourmis in listFourmis:
				#Tant que la fourmi n'est pas arrivée à destination, elle avance
				while(fourmis.getNoeudCourant() != fin) :
					fourmis.avancer(self,alpha,beta,gamma)

			#Une fois que toutes les fourmis sont arrivées, elles répendent chacune leurs phéromones en fonction de la piste parcouru
			for fourmis in listFourmis :
				self.matPheromones = fourmis.rependrePheromone(self.matPheromones)
				fourmis.reinitialiser(debut)
			#On simule un evaporation
			self.evaporation(pho)

		#On retrouve le chemin le plus petit à l'aide de l'intensité des phéromones
		plusCourtChemin = []
		plusCourtChemin.append(debut)
		max = 0
		#On choisi à chaque fois l'arrête ayant la plus forte intensité de phéromones
		while(plusCourtChemin[-1] != fin):
			for i in range(1,len(self.matPheromones[plusCourtChemin[-1]])):
				if(self.matPheromones[plusCourtChemin[-1]][max] <= self.matPheromones[plusCourtChemin[-1]][i] and self.matPheromones[plusCourtChemin[-1]][i] != -1 and i not in plusCourtChemin):
					max = i
			tmp = plusCourtChemin[-1]
			plusCourtChemin.append(max)	
			#On met a 0 le chemin sur lequel on vient de passer pour être sûr de ne pas y repasser
			self.matPheromones[tmp][plusCourtChemin[-1]] = 0
			self.matPheromones[plusCourtChemin[-1]][tmp] = 0
			max = 0 

		return plusCourtChemin

	#Simule une evaporation de pho % de phéromones sur chaque arretes
	def evaporation(self,pho = 0.1):
		for successeur in range(0,len(self.matPheromones)):
			for predecesseur in range(0,len(self.matPheromones[0])):
				if(self.matPheromones[successeur][predecesseur] != -1):
					#evaporation de pho/2 (deux evaporation par arrête une fois de A vers B et une autre fois de B vers A)
					self.matPheromones[successeur][predecesseur] = self.matPheromones[successeur][predecesseur] - (self.matPheromones[successeur][predecesseur] * (pho/2))


	#Retourne la matrice représentant les distances sur les arrêtes
	def getMatDistances(self):
		return self.matDistances

	#Retourne la matrice représentant les pheromones sur les arrêtes
	def getMatPheromones(self):
		return self.matPheromones

	#Retourne les voisins d'un noeud 
	def getVoisin(self,node):
		voisin = []
		#Pour chaque prédécesseur
		for predecesseur in range(0,len(self.matDistances[node])):
			#Si il y a une valeur autre que -1 dans la matrice :
			if(self.matDistances[node][predecesseur] != -1 ):
				voisin.append(predecesseur)
		#On renvoie la liste des voisins
		return voisin

	#Affiche la matrice dans le terminal
	def afficherMatDistance(self):
		for successeur in range(0,len(self.matDistances)):
			tmp = " | "
			for predecesseur in range(0,len(self.matDistances[0])):
				tmp = tmp + str(self.matDistances[successeur][predecesseur]) + "  "
			print(tmp + " | \n")



	
