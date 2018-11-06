from tkinter import *
from numpy import random as rd
from PIL import Image, ImageTk
import winsound as ws
import time

#Variables
        
h = 600 #Hauteur de la fenêtre
w = 600 #Largeur de la fenêtre

c = 20 #Largeur du joueur/Ennemis de base

xj = w/2-c/2 #Abscisse du joueur
yj = h/2-c/2 #Ordonnée du joueur
vj = 1 #Vitesse du joueur
bonusJ = [0]
bonusTimes = [0]

vitesse=5 #Vitesse de l'animation

flag=0 #Pause ou non du jeu

eventsFleches = [0,0,0,0] #Tableau des flèches pressées (1) ou non (0)

rnd = 1

vague = 0
son = 'PasBoss'

nbrE = 0 #Nombre d'ennemis dans la vague
xE = [] #Abscisse des ennemis de la vague
yE = [] #Ordonnée des ennemis de la vague
etatE = [] #Ennemi vivant (1) ou mort (0)
typeE = [] #Type de l'ennemi 
vE = [] #Vitesse des ennemis
couleurE = [] #Couleur des ennemis (en fonction du type)
debutE = [] #Date de création des ennemis (pour les Speeders par exemple)

def go():
    "démarrage de l'animation"
    global flag
    if flag == 0:
        flag = 1
        play()
        
def stop():
    "arrêt de l'animation"
    global flag    
    flag = 0
    
def play(): 
    global flag, vitesse

    bouclePrincipale()
    
    if flag >0: 
        fen1.after(vitesse,play)

def EnnemisVivants():
    global etatE, nbrE

    for i in range(nbrE):
        if etatE[i] and not typeE[i]==101:
            return 1
    return 0

def reinitE():
    global nbrE, xE, yE, etatE, typeE, vE, couleurE, debutE
    
    xE = []
    yE = []
    etatE = []
    typeE = []
    vE = []
    couleurE = []
    debutE = []

def JoueurPasAuBord():
    global xj, yj, vj, h, w
    if xj <= w/4:
        xj += vj
        return False
    elif xj >= 3*w/4-c:
        xj -= vj
        return False
    elif yj <= h/4:
        yj += vj
        return False
    elif yj >= 3*h/4-c:
        yj -= vj
        return False
        
    return True

def YacollisionE():
    global xj, yj
    global nbrE, xE, yE

    for i in range(nbrE):
        if ( xE[i]+c>xj and xE[i]+c<xj+c and yE[i]+c>yj and yE[i]+c<yj+c ):
            return i+1
        elif ( xE[i]+c>xj and xE[i]+c<xj+c and yE[i]>yj and yE[i]<yj+c ):
            return i+1
        elif ( xE[i]>xj and xE[i]<xj+c and yE[i]+c>yj and yE[i]+c<yj+c ):
            return i+1
        elif ( xE[i]>xj and xE[i]<xj+c and yE[i]>yj and yE[i]<yj+c ):
            return i+1
    return 0

def BalanceMerdouille():
    global vague, rnd
    global nbrE, xE, yE, etatE, typeE, debutE, couleurE

    if rnd==10:
        nbrE+=1
        if (nbrE-1)%(4+3*vague)==0:
            typeE.append(1010)
            couleurE.append('blue')
        else:
            typeE.append(0)
            couleurE.append('red')
        etatE.append(1)
        yE.append(-c)
        xE.append(rd.randint(0,w-c))
        vE.append(1+0.1*rnd+0.02*vague)
        debutE.append(time.time())
        
        fen1.after(600-vague*60,BalanceMerdouille)


def NouvelleVague():
    global rnd, vague
    global nbrE, xE, yE, etatE, typeE, debutE, couleurE
    global bonusJ
    global son

    reinitE()

    if vague==5:
        vague = 1
        rnd += 1
        bonusJ[0] = 0
        if rnd%10==0:
            ws.PlaySound("100_Rounds_Boss.wav", ws.SND_ASYNC)
            son = 'boss'
        elif son == 'boss':
            ws.PlaySound("100_Rounds_Music.wav", ws.SND_ASYNC)
            son = 'PasBoss'
    else:
        vague += 1

    if rnd<3:
        nbrE = 5 + 2*rnd + vague

        for i in range(nbrE):
            typeE.append(rd.randint(0,4)*10)
            etatE.append(1)
            if typeE[i]==0:
                yE.append(-c)
                xE.append(rd.randint(0,w-c))
            elif typeE[i]==10:
                yE.append(h)
                xE.append(rd.randint(0,w-c))
            elif typeE[i]==20:
                yE.append(rd.randint(0,h-c))
                xE.append(-c)
            elif typeE[i]==30:
                yE.append(rd.randint(0,h-c))
                xE.append(w)
            vE.append(1+0.1*rnd+0.02*vague)
            couleurE.append('red')
            debutE.append(time.time())
    elif rnd>=3 and rnd<5:
        nbrE = rnd + vague + 1

        for i in range(nbrE):
            typeE.append(rd.randint(4,8)*10)
            etatE.append(1)
            alea = rd.randint(0,2)
            if typeE[i]==40:
                if alea:
                    yE.append(rd.randint(0,(h-c)/2))
                    xE.append(-c)
                else:
                    xE.append(rd.randint(0,(w-c)/2))
                    yE.append(-c)
            elif typeE[i]==50:
                if alea:
                    yE.append(rd.randint((h-c)/2,(h-c)))
                    xE.append(w)
                else:
                    xE.append(rd.randint((w-c)/2,(w-c)))
                    yE.append(h)
            elif typeE[i]==60:
                if alea:
                    yE.append(rd.randint((h-c)/2,(h-c)))
                    xE.append(0)
                else:
                    xE.append(rd.randint(0,(w-c)/2))
                    yE.append(h)
            elif typeE[i]==70:
                if alea:
                    yE.append(rd.randint(0,(h-c)/2))
                    xE.append(w)
                else:
                    xE.append(rd.randint((w-c)/2,(w-c)))
                    yE.append(0)
            vE.append(1+0.05*rnd+0.02*vague)
            couleurE.append('orange')
            debutE.append(time.time())
    elif (rnd>=5 and rnd<10) or rnd>10:
        nbrE = 5 + 2*(rnd-6) + vague
        
        for i in range(nbrE):
            typeE.append(rd.randint(0,4)*10+1)
            etatE.append(1)
            if typeE[i]==1:
                yE.append(-c)
                xE.append(rd.randint(0,w-c))
            elif typeE[i]==11:
                yE.append(h)
                xE.append(rd.randint(0,w-c))
            elif typeE[i]==21:
                yE.append(rd.randint(0,h-c))
                xE.append(-c)
            elif typeE[i]==31:
                yE.append(rd.randint(0,h-c))
                xE.append(w)
            vE.append(1+0.1*(rnd-6)+0.02*vague)
            couleurE.append('lightgreen')
            debutE.append(time.time())
    elif rnd==10:
        "Création du boss"
        nbrE = 1
        typeE.append(101)
        etatE.append(1)
        vE.append(0)
        xE.append(w/2-50)
        yE.append(100)
        debutE.append(time.time())
        couleurE.append("purple")
        "Création des merdouilles"
        BalanceMerdouille()
        
    if rnd%10==0:
        texteRound.config(text="Round "+str(rnd)+" Boss "+str(rnd//10))
    else:
        texteRound.config(text="Round "+str(rnd)+" Vague "+str(vague))

def BougeageEnnemis():
    global rnd, vague
    global nbrE, xE, yE, etatE, typeE, vE, debutE

    for i in range(nbrE):
            if (etatE[i]):
                if typeE[i]==1 or typeE[i]==11 or typeE[i]==21 or typeE[i]==31:
                    if time.time()>=debutE[i]+0.8*vE[i]:
                        vE[i]*=2.5
                        
                if typeE[i]==0 or typeE[i]==1 or typeE[i]==1010:
                    yE[i]+=vE[i]
                elif typeE[i]==10 or typeE[i]==11:
                    yE[i]-=vE[i]
                elif typeE[i]==20 or typeE[i]==21:
                    xE[i]+=vE[i]
                elif typeE[i]==30 or typeE[i]==31:
                    xE[i]-=vE[i]
                elif typeE[i]==40:
                    xE[i]+=vE[i]
                    yE[i]+=vE[i]
                elif typeE[i]==50:
                    xE[i]-=vE[i]
                    yE[i]-=vE[i]
                elif typeE[i]==60:
                    xE[i]+=vE[i]
                    yE[i]-=vE[i]
                elif typeE[i]==70:
                    xE[i]-=vE[i]
                    yE[i]+=vE[i]
                    

            if xE[i]>w or xE[i]+c<0 or yE[i]>h or yE[i]+c<0:
                etatE[i]=0
    
def BonusVitesseJ():
    global bonusJ, bonusTimes
    
    if bonusJ[0] == 0:
        bonusJ[0] = 1
        bonusTimes[0] = time.time()
        texteBonus.config(text="Bonus Vitesse Activé")

        
def bouclePrincipale(): #On efface et on redessine tout
    global fond
    global xj, yj, vj
    global rnd, vague
    global nbrE, xE, yE, etatE, typeE, vE
    global bonusJ, bonusTimes

    vjLocal = 0
    
    can1.delete(ALL) #Effacage

    "On regarde si y'a des bonus d'activés ou à désactiver"
    if bonusJ[0]==1:
        if time.time()-bonusTimes[0]>3:
            bonusJ[0]=2
            vjLocal = vj
            texteBonus.config(text="")
        else:
            vjLocal = 2*vj
    else:
        vjLocal = vj

    "Changement des coordonnées du joueur"
    if JoueurPasAuBord():
        if (eventsFleches[0]==1):
            xj-=vjLocal
        if (eventsFleches[1]==1):
            yj-=vjLocal
        if (eventsFleches[2]==1):
            xj+=vjLocal
        if (eventsFleches[3]==1):
            yj+=vjLocal


    "Gestion du round, des vagues et des ennemis"
    if EnnemisVivants():
        BougeageEnnemis()
    else:
        NouvelleVague()
    
    "Perdu"
    ennemiTouche = YacollisionE()
    if ennemiTouche:
        if typeE[ennemiTouche-1]==1010:
            NouvelleVague()
        else:
            stop()
            texteRound.config(text="PERDU !")
            ws.PlaySound("100_Rounds_Fin", ws.SND_ASYNC)


    "Affichage"
    can1.create_image(400,300, image=fond) #Affichage du fond
    can1.create_rectangle(xj, yj, xj+c, yj+c, fill='blue') #Affichage du joueur

    for i in range (nbrE): #Affichage des ennemis
        if typeE[i]==101:
                can1.create_rectangle(270, 45, 330, 105, fill="purple")
        elif etatE[i]:
            if typeE[i]==1010:
                can1.create_oval(xE[i], yE[i], xE[i]+c, yE[i]+c, fill=couleurE[i])
            else:
                can1.create_rectangle(xE[i], yE[i], xE[i]+c, yE[i]+c, fill=couleurE[i])
        

def touchePressée(evt0):
    for i in range(4):
        if evt0.keycode==(37+i):
            eventsFleches[i]=1
        if evt0.keysym=='b':
            BonusVitesseJ()
        if evt0.keysym=='p':
            stop()
        if evt0.keysym=='g':
            go()

def toucheLachée(evt0):
    for i in range(4):
        if evt0.keycode==(37+i):
            eventsFleches[i]=0

#Main

fen1 = Tk()

fen1.title("100 Rounds")

imgtemp = Image.open("image_fond.jpg") 
fond = ImageTk.PhotoImage(imgtemp)

can1 = Canvas(fen1, width =w, height =h, bg ='white')
can1.pack(side = TOP)
can1.create_image(400,300, image=fond)

texteRound=Label(fen1, text="Round 1 Vague 1", font="Arial 25", width = 15)
texteRound.pack(side = LEFT)
texteBonus=Label(fen1, text="", font="Arial 15", pady=6)
texteBonus.pack()

fen1.bind("<KeyPress>", touchePressée)
fen1.bind("<KeyRelease>", toucheLachée)

go()

ws.PlaySound("100_Rounds_Music.wav", ws.SND_ASYNC)

fen1.mainloop()
