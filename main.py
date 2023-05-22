from tkinter import *
import csv
from math import sqrt


# Variables
x = 0
y = 0
T = []
X = []
Y = []
type = [["eau", "#2581ee"], ["roche", "#b1ab82"], ["feu", "#e72324"], ["plante", "#3da224"], ["insecte", "#93a213"], ["electrique", "#fbc101"], ["dragon", "#4f61e3"], ["poison", "#923fcc"], ["glace", "#3cd9fe"]]

  #########################################################
 #                                                         #
 #                     ~ FONCTIONS ~                       #
 #                                                         #
  #########################################################

def getClickCoord(event):
    return event.x, event.y

def updateCoordLabels(event):
    coords = getClickCoord(event)

    xLabel.config( text=f"x : {coords[0]}" )
    yLabel.config( text=f"y : {coords[1]}" )

# KNN
def chargement(nomfichier) :
#Lecture du fichier CSV contenant les types d'objets et leurs coordonnées
#on cree 3 listes qui vont contenir : le type, l'abscisse, et l'ordonnée
    with open(nomfichier,"r") as fichier:
        #ouvrir votre fichier pour vérifier si vos champs sont délimités
        #par une virgule ou un point virgule
        doc_a_lire = csv.reader(fichier, delimiter=",")
        #chaque ligne va être lue, séaprées en 3 et les listes MAJ
        for ligne in doc_a_lire:
            T.append(int(ligne[0]))
            X.append(float(ligne[1]))
            Y.append(float(ligne[2]))
    return T,X,Y

def distance(Xr, Yr):
    dist = []
    for i in range(len(T)):
        d = (X[i] - Xr)**2 + (Y[i] - Yr)**2
        d = sqrt(d)
        dist.append([d, T[i]])
    
    return dist

def k_voisins(Dist, k): #k est le nombre de voisins a prendre en compte
    # trier la liste Dist en fonction de Dist[0] => distance
    for i in range(1, len(Dist)):
        tmp = Dist[i]
        j = i
        while j > 0 and Dist[j-1][0] > tmp[0]:
            Dist[j] = Dist[j-1]
            j -= 1
        Dist[j] = tmp

    # append les k premiers dans voisin
    voisin = []
    for i in range(k):
        voisin.append(Dist[i])
    
    return voisin

def predire_classeV1(voisin):
    prediction = 'je sais pas pour le moment'
    t = [0 for i in range(len(voisin))]

    iMax = 0
    max = t[0]
    for i in range(1, len(t)):
        if t[i] > max:
            max = t[i]
            iMax = i

    prediction = iMax

    return prediction

def predire_classe(voisin):
    t = [0 for i in range(9)]

    for i in voisin:
        t[i[1]] += 1
    
    iMax = 0
    max = t[0]
    for i in range(1, len(t)):
        if t[i] > max:
            max = t[i]
            iMax = i
    
    return iMax
       
        

def KNN(event):
    pred = "non"

    updateCoordLabels(event)

    coords = getClickCoord(event)

    dist = distance(coords[0], coords[1])

    k = kSlider.get()
    voisins = k_voisins(dist, k)
    pred = predire_classe(voisins)

    resultLabel.config( text=f"Dans cette zone, vous croiserez\n probablement des pokemons du type :" )
    typeLabel.config(text=type[pred][0], fg=type[pred][1])



  #########################################################
 #                                                         #
 #                ~ PROGRAMME PRINCIPALE ~                 #
 #                                                         #
  #########################################################

# Instanciation de la fenêtre
fen = Tk()
fen.geometry("600x335")
fen.minsize(660, 335)
fen.maxsize(660, 335)

colLeft = Frame(fen, width="425")
# Affichage de la carte
carte = PhotoImage(file="map_pokeland.png")
carteLabel = Label(colLeft, image=carte)
carteLabel.pack()

# Status line
statusFrame = Frame(colLeft)
coordFrame = Frame(statusFrame)

xLabel = Label(coordFrame, text=f"x : {x}")
yLabel = Label(coordFrame, text=f"y : {y}")
xLabel.pack(side = LEFT)
yLabel.pack(side = RIGHT, padx=15)

coordFrame.pack(side = LEFT)

# City name
cityName = "Johto"
cityNameLabel = Label(statusFrame, text="")
cityNameLabel.pack(side = RIGHT, padx=150)

statusFrame.pack()

colLeft.pack( side = LEFT )

colRigth = Frame(fen)

kFrame = Frame(colRigth)
# Affichage du slider k
kLabel = Label(kFrame, text="Nombre de voisin :")
kLabel.pack()

kSlider = Scale(kFrame, from_=1, to=42, orient=HORIZONTAL)
kSlider.pack( padx=65 )

kFrame.pack( pady=30 )

# Affichage du résultat de l'algo KNN
resultLabel = Label(colRigth, text="")
resultLabel.pack()

typeLabel = Label(colRigth, text="", font=("", 18))
typeLabel.pack( pady=5 )


colRigth.pack( side = RIGHT )

# bind event pour avoir la prediction de l'algo KNN
carteLabel.bind("<Button-1>", KNN)

chargement("data.csv")

fen.mainloop()

