#!/usr/bin/python3
from Graph import *
import time
from optparse import OptionParser
#converti un int en char ex: 0-> A, 3->D...
def intToChar(int):
		return chr(int + 97).upper()

#Genere une image du graphe à partir d'une matrice
#Converti la matrice en un fichier dot
def genererGraphe(matDistances,chemin,filename) :
	graph = "strict graph  { \n "
	#Pour chaque lien entre les noeuds
	for successeur in range(0,len(matDistances)):
		for predecesseur in range(0,len(matDistances[0])):
			val = matDistances[successeur][predecesseur]
			if(val != -1):
				#On créé le lien dans le fichier dot
				if(successeur in chemin and ( (chemin.index(successeur) < len(chemin)-1 and predecesseur == chemin[chemin.index(successeur)+1]) or (chemin.index(successeur) > 0 and predecesseur == chemin[chemin.index(successeur)-1]))):
					graph = graph + intToChar(successeur) +" -- "+intToChar(predecesseur) + " [penwidth = 2.5, color=red,label="+str(val)+",weight="+str(val)+"]; \n "
				elif(predecesseur in chemin and ( (chemin.index(predecesseur) > 0 and successeur == chemin[chemin.index(predecesseur)-1]) or (chemin.index(predecesseur) < len(chemin)-1  and successeur == chemin[chemin.index(predecesseur)+1]))):
					graph = graph + intToChar(successeur) +" -- "+intToChar(predecesseur) + " [penwidth = 2.5, color=red,label="+str(val)+",weight="+str(val)+"]; \n "
				else:
					graph = graph + intToChar(successeur) +" -- "+intToChar(predecesseur) + " [penwidth = 2,color=blue,label="+str(val)+",weight="+str(val)+"]; \n "
	graph = graph + "}"
	#print("Fichier .dot : \n "+graph) #Affiche sur le terminal le ficheir dot
	f = open("graph.dot", "w")
	f.write(graph) #On ecrit les donnees dans un fichier dot
	f.close()
	subprocess.Popen("dot -Tpng graph.dot -o "+filename,shell=True,stdout=subprocess.PIPE) #grace à la commande dot, on génere le png
	print("\n"+filename+" généré. Ouvrez le pour visualiser le graphe et son plus court chemin \n")


#Parametre par defaut
#Matrice par defaut si une matrice n'a pas été  passé en parametre
#Matrice de test :
# [[-1,2,7],[2,-1,3],[7,3,-1]]
# [[-1,3,-1,9],[3,-1,2,7],[-1,2,-1,2],[9,7,2,-1]]
# [[-1,5,-1,1],[5,-1,-1,3],[-1,-1,-1,3],[1,3,3,-1]]
# [[-1,6,10,-1,8],[6,-1,2,8,-1],[10,2,-1,5,-1],[-1,8,5,-1,7],[8,-1,-1,7,-1]]
#Graphe complet : [[-1,7,11,12,9,2],[7,-1,5,1,13,3],[11,5,-1,2,1,9],[12,1,2,-1,6,10],[9,13,1,6,-1,18],[2,3,9,10,18,-1]]
#Graohe complet : [[-1,2,8,12,7],[2,-1,7,8,3],[8,7,-1,2,1],[12,8,2,-1,4],[7,3,1,4,-1]]
matriceParDefaut = [[-1,2,8,12,7],[2,-1,7,8,3],[8,7,-1,2,1],[12,8,2,-1,4],[7,3,1,4,-1]]
depart = "0"
dest = "2"


#Parser les options en entré du programme
parser = OptionParser()
parser.add_option("-o", "--output", dest="output", default="graphe.png", help="Fichier png en sortie. Par defaut : graph.png", metavar="FILE")
parser.add_option("-s", "--source", dest="source", default=depart, help="Point de départ pour trouver le plus court chemin entre 0 et nbnoeuds-1 ou une lettre (a = 0, c = 2....)")
parser.add_option("-d", "--dest", dest="dest", default=dest, help="Point d'arrivé pour trouver le plus court chemin entre 0 et nbnoeuds-1 ou une lettre (a = 0, c = 2....)")
option_dict = vars(parser.parse_args()[0])
#Traitement des option destination et source
if option_dict["source"].isalpha():
	source = ord(option_dict["source"].upper()) - 65
else:
	source = int(option_dict["source"])

if option_dict["dest"].isalpha():
	dest = ord(option_dict["dest"].upper()) - 65
else:
	dest = int(option_dict["dest"])

#Construction du graphe
#Matrice passée en parametre du graphe ou matrice par défaut
graph = Graph(matriceParDefaut)
#Affichage de la matrice dans le terminal
graph.afficherMatDistance()
#Si la matrice est valide ainsi que les noeuds source et destination, on génère le graphe
if(graph.matValide() and len(matriceParDefaut) > source and len(matriceParDefaut) > dest):
	#On trouve le plus court chemin avec la fonction shortestPathACO 
	tps1 = time.time()
	plusCourtChemin = graph.shortestPathACO(source,dest,50,0.1,1,1,1,100)
	tps2 = time.time()
	print("Temps d'execution du programme : "+ str(tps2 - tps1) + " secondes")
	#On genere le PNG du graphe avec le plus court chemin trouvé
	genererGraphe(graph.getMatDistances(),plusCourtChemin,option_dict["output"])
	#Affichage du plus court chemin dans le terminal
	print("Chemin le plus court entre "+intToChar(source)+" et "+intToChar(dest)+" \n ")
	print(str(list(map(lambda i: intToChar(i), plusCourtChemin))))
else:
	print("Erreur options invalide")

