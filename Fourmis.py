import os, subprocess, sys, random
import copy
class Fourmis :

	def __init__(self,noeudDepart):
		self.distanceParcouru = 0 
		self.cheminParcouru = []
		self.cheminParcouru.append(noeudDepart)

	#Renvoie le noeud sur lequel la fourmi se trouve
	def getNoeudCourant(self):
		#Le dernier noeud du chemin parcouru est le noeud sur lequel la fourmi se trouve.
		return self.cheminParcouru[-1]

	#Renvoie la fourmi au point de départ
	def reinitialiser(self,noeudDepart):
		self.distanceParcouru = 0 
		self.cheminParcouru = [noeudDepart]

	#Répends une quantité de phéromones sur le chemin emprunté en fonction de la distance parcouru par la fourmi
	def rependrePheromone(self,matPheromones,Q = 1):
		#On calcul la distance parcouru par la fourmis
		delta = (Q/self.distanceParcouru)
		for i in range(0,len(self.cheminParcouru)-1):
			matPheromones[self.cheminParcouru[i]][self.cheminParcouru[i+1]] += delta
			matPheromones[self.cheminParcouru[i+1]][self.cheminParcouru[i]] += delta
		return matPheromones

	#Fonction permettant de faire avancer la fourmi au prochain noeud en fonction des chemins disponibles, des phéromones et de parametres aleatoires
	def avancer(self,graphe,alpha = 1 ,beta = 1 ,gamma = 1):
		#On recupère la liste des deplacements
		deplacementPossible = graphe.getVoisin(self.getNoeudCourant())

		#Si on est dans un chemin sans issue on retourne en arrière (cela reviens à enlever le dernier noeud, cela permettra que les chemins sans issue n'aient pas de phéromones
		#Pas besoin de MAJ les distances et le chemin
		if (len(deplacementPossible) == 1 and len(self.cheminParcouru) != 1):
			self.cheminParcouru.pop(-1)
			return 0

		#On enleve le noeud d'où l'on vient dans les choix possibles
		if len(self.cheminParcouru) >= 2 :
			deplacementPossible.pop(deplacementPossible.index(self.cheminParcouru[len(self.cheminParcouru)-2]))

		#Calcul du numerateur de la règle aléatoire de transition proportionnelle
		listTransitionProp = list(map(lambda i: (graphe.getMatPheromones()[self.getNoeudCourant()][i] ** alpha) / (graphe.getMatDistances()[self.getNoeudCourant()][i] ** beta), deplacementPossible))
		#Calcul du denominateur de la règle aléatoire de transition proportionnelle
		sumTransProp = sum(listTransitionProp)
		#Calcul de la règle aléatoire de transition proportionnelle
		listTransitionProp = list(map(lambda i: (i/sumTransProp),listTransitionProp))

		#Roulette Russe pour choisir un chemin en fonction de la regle aléatoire de transition proportionnelle
		roulette = random.random() 
		for i, chance in enumerate(listTransitionProp):
			roulette -= chance
			if(roulette < 0):
				idxcheminChoisi = i
				cheminChoisi = deplacementPossible[idxcheminChoisi]
				break

		#Mis a jour du chemin de la fourmi
		self.distanceParcouru += graphe.getMatDistances()[self.getNoeudCourant()][cheminChoisi]
		self.cheminParcouru.append(cheminChoisi)
		return 0
