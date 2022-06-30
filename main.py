from tkinter import*
from tkinter import messagebox
from random import*


class Case:

    def __init__(self,x,y) :
        self.x = x
        self.y = y
        self.mine = False
        self.mine_voisine = 0
        self.decouverte =False
        self.deminer = False

class Grille:

    def __init__(self) :
        self.contenue = [[] for i in range(16) ]
        self.loose = False
        self.win = False
        self.liste_mine = []
        self.nb_a_deminer = 40

    def compte_mine(self,x, y):

        if x != 0 and x != 15 and y != 0 and y != 15:
            for i in range(y - 1, y + 2):
                for j in range(x - 1, x + 2):
                    print([x,y],[i,j])
                    if self.contenue[i][j].mine:
                        self.contenue[y][x].mine_voisine += 1
        if x == 0 and y == 0 :
            for i in range(y,y+2):
                for  j in range(x,x+2):
                    if self.contenue[i][j].mine:
                        self.contenue[y][x].mine_voisine += 1
        if x == 15 and y == 0 :
            for i in range(y,y+2):
                for j in range(15,13,-1):
                    if self.contenue[i][j].mine:
                        self.contenue[y][x].mine_voisine += 1
        if x == 15 and y == 15 :
            for i in range(15, 13 , -1):
                for j in range(15, 13, -1):
                    if self.contenue[i][j].mine:
                        self.contenue[y][x].mine_voisine += 1
        if x == 0 and y == 15 :
            for i in range(15, 13 , -1):
                for j in range(x, x+2):
                    if self.contenue[i][j].mine:
                        self.contenue[y][x].mine_voisine += 1
        if x != 0 and x!=15 and y == 0 :
            for i in range(y, y + 2):
                for j in range(x-1,x+2):
                    if self.contenue[i][j].mine:
                        self.contenue[y][x].mine_voisine += 1
        if x==15 and y!=0 and y!=15:
            for i in range(y-1, y + 2):
                for j in range(15,13,-1):
                    if self.contenue[i][j].mine:
                        self.contenue[y][x].mine_voisine += 1

        if x != 0 and x != 15 and y == 15:
            for i in range(y, y-2 , -1):
                for j in range(x-1,x+2):
                    if self.contenue[i][j].mine:
                        self.contenue[y][x].mine_voisine += 1
        if x == 0 and y != 0 and y != 15 :
            for i in range(y-1, y +2):
                for j in range(x, x+2):
                    if self.contenue[i][j].mine:
                        self.contenue[y][x].mine_voisine += 1

    def remplir(self) :

        #Rempli la grille de case basique
        for y in range(16) :
            for x in range(16) :
                self.contenue[y].append(Case(x,y))

        #Pose des mines aléatoirement
        mine = 0
        while mine < 40:
            a = randint(0, 15)
            b = randint(0, 15)
            if not self.contenue[a][b].mine:
                self.contenue[a][b].mine = True
                mine += 1
                self.liste_mine.append(self.contenue[a][b])

        #Compte les mines voisines
        for y in range(16):
            for x in range(16):
                self.compte_mine(x,y)


def propagation(x,y):
    demineur.contenue[y][x].decouverte = True
    if x != 0 and x != 15 and y != 0 and y != 15:
        if not demineur.contenue[y][x].mine and demineur.contenue[y][x].mine_voisine == 0 :
            for i in range(y-1,y+2):
                for j in range(x-1,x+2):
                    if not demineur.contenue[i][j].decouverte:
                        propagation(j,i)
    if x == 0 and y == 0 :
        if not demineur.contenue[y][x].mine and demineur.contenue[y][x].mine_voisine == 0 :
            for i in range(y,y+2):
                for j in range(x,x+2):
                    if not demineur.contenue[i][j].decouverte:
                        propagation(j,i)
    if x == 15  and  y == 0:
        if not demineur.contenue[y][x].mine and demineur.contenue[y][x].mine_voisine == 0 :
            for i in range(y,y+2):
                for j in range(15,13,-1):
                    if not demineur.contenue[i][j].decouverte:
                        propagation(j,i)
    if x == 15  and  y == 15:
        if not demineur.contenue[y][x].mine and demineur.contenue[y][x].mine_voisine == 0 :
            for i in range(15,13,-1):
                for j in range(15,13,-1):
                    if not demineur.contenue[i][j].decouverte:
                        propagation(j,i)

def leftClick(event):

    canvas.delete('all')
    x = event.x // 40
    y = event.y // 40

    if demineur.contenue[y][x].deminer:
        return affiche()

    demineur.contenue[y][x].decouverte = True
    if demineur.contenue[y][x].mine:
        demineur.loose = True
        for ligne_case in demineur.contenue:
            for case in ligne_case:
                case.decouverte = True

    if not demineur.contenue[y][x].mine and demineur.contenue[y][x].mine_voisine == 0 :
        propagation(x,y)
    if not demineur.loose and not demineur.win:
        affiche()

    elif demineur.loose:
        affiche()
        messagebox.showerror("PERDU :(", "VOUS AVEZ PERDU")
        print('perdu')

def rightClick(event):
    canvas.delete('all')
    x = event.x // 40
    y = event.y // 40

    if demineur.contenue[y][x].decouverte :
        return affiche()
    if demineur.contenue[y][x].deminer :
        demineur.contenue[y][x].deminer = False
        if demineur.contenue[y][x] in demineur.liste_mine:
            demineur.nb_a_deminer += 1
        else:
            demineur.nb_a_deminer -= 1
    else:
        demineur.contenue[y][x].deminer = True
        if demineur.contenue[y][x] in demineur.liste_mine:
            demineur.nb_a_deminer -= 1
        else :
            demineur.nb_a_deminer += 1

    print(demineur.nb_a_deminer)

    if demineur.nb_a_deminer == 0:
        demineur.win = True
        for ligne_case in demineur.contenue:
            for case in ligne_case:
                case.decouverte = True
    if not demineur.loose and not demineur.win:
        affiche()
    elif demineur.win:
        affiche()
        messagebox.showinfo("VICTOIRE !", "VOUS AVEZ GAGNÉ")
        print('gagné')

def affiche():

    for y in range(16):
        for x in range(16):
            a = demineur.contenue[y][x].x
            b = demineur.contenue[y][x].y
            voisin = demineur.contenue[y][x].mine_voisine

            if not demineur.contenue[y][x].decouverte and not demineur.contenue[y][x].deminer :
                button  = canvas.create_image(x * 40, y * 40, image=imageButton, anchor='nw', activeimage = imageButtonActive )

            elif demineur.contenue[y][x].deminer  :
                flag = canvas.create_image(x*40 , y*40 , image = imageFlag , anchor ='nw')

            elif demineur.contenue[y][x].decouverte:

                if demineur.contenue[y][x].mine:

                    bomb = canvas.create_image(x*40 , y*40 , image = imageBomb  , anchor ='nw')

                else:

                    number = canvas.create_image(x*40 , y*40 , image = imageNb[voisin]  , anchor ='nw')

            if demineur.contenue[y][x].deminer and demineur.loose and not demineur.contenue[y][x].mine:

                    notBomb = canvas.create_image(x*40 , y*40 , image = imageNotBomb  , anchor ='nw')





demineur = Grille()
demineur.remplir()
window = Tk()
window.geometry("650x650")
canvas = Canvas(window, width=640, height=640)
canvas.pack()
pixelVirtual = PhotoImage(width=1,height=1)
imageButton = PhotoImage(file = "assets/button.png")
imageButtonActive = PhotoImage(file="assets/buttonactive.png")
imageBomb = PhotoImage(file = "assets/mine.png")
imageNotBomb = PhotoImage(file = "assets/notMine.png")
imageFlag = PhotoImage(file = "assets/flag.png")
imageNb = [PhotoImage(file = "assets/"+str(i)+".png") for i in range(7)]
affiche()
canvas.bind("<Button-1>",leftClick)
canvas.bind("<Button-3>",rightClick)
window.mainloop()
