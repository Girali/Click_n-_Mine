# -*- coding: cp1250 -*-
import pygame
from pygame.locals import *
from pygame import*
import time
import sqlite3
from random import*

pygame.init()

clock = pygame.time.Clock()

fenetreL = 800
fenetreH = 600

logo_y = 100

fenetre = pygame.display.set_mode((fenetreL, fenetreH))#fenetre
pygame.display.set_caption('Click and Mine')


icon = pygame.image.load('data/icon.png')#icon
pygame.display.set_icon(icon)


pygame.mixer.music.load("sound/music.mp3")#musique
pygame.mixer.music.play(-1)

white = 255,255,255 #couleur
green = 0,178,0
yellow = 217,200,0
black = 0,0,0
red = 150,30,0
blue = 0,0,0

font_petit = pygame.font.Font("data/police2.ttf",24)#police
font_grand = pygame.font.Font("data/police2.ttf",34)
font = pygame.font.Font('data/police.ttf', 24)

fond = pygame.image.load("image/magazin/selection_shop.png").convert_alpha()#Définitions des images utiliser dans les magazins
back = pygame.image.load('image/menu/back.png')

profil = 1

click = True

#valeurs a event
delay = 10800 # car 60 FPS donc 3 * 60 * 60 = 10800 (3 min)
fun = 4
double = False
divise = False


#db
conn = sqlite3.connect('data/data.db')#initialisation de la base de donner
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS stuffToPlot(nb_profil REAL, money REAL, player_power_up REAL, player_power_up_ REAL, npc_one REAL, npc_two REAL, npc_three REAL, npc_four REAL, npc_five REAL, npc_six REAL, npc_seven REAL, npc_height REAL)')


#INDEX DES VALEURS
#   money == l'argent (global)
#   profil == a declarer dans tous les fonctions utilisant la base de donnee
#   cps == l'argent par second
#
#
#
#
#
#
#
#

#LE PLAYER
class Player():
    #les donnes de bases
    def __init__(self,x,y):
        self.x = x #position X
        self.y = y #position Y
        self.jump = False #Sol
        self.gravity = 0 #Velocitee de la gravitee
        self.side_left = True#si regarde en derrnier a gauche
        self.move = False#si en mouvement
        #importation de sprite
        self.player_left = pygame.image.load('animation/player_left.png')
        self.player_right = pygame.image.load('animation/player_right.png')
        self.ani_left = (pygame.image.load('animation/hr1.png').convert_alpha(),
                         pygame.image.load('animation/hr2.png').convert_alpha(),
                         pygame.image.load('animation/hr3.png').convert_alpha(),
                         pygame.image.load('animation/hr4.png').convert_alpha())
        self.ani_right = (pygame.image.load('animation/hl1.png').convert_alpha(),
                         pygame.image.load('animation/hl2.png').convert_alpha(),
                         pygame.image.load('animation/hl3.png').convert_alpha(),
                         pygame.image.load('animation/hl4.png').convert_alpha())
        self.player_jump_left = pygame.image.load('animation/playerjumpl.png').convert_alpha()
        self.player_jump_right = pygame.image.load('animation/playerjumpr.png').convert_alpha()
        self.init_frame = 6#varibale pour aniamtion
        self.frame = self.init_frame
        self.sprite = 0

    #verifier si au sol
    def ground (self):
        if self.y >= 516:
            self.y = 516
            self.jump = False
        else:
            self.jump = True
            
    #la gravitee 
    def update(self, gravity):
        if self.jump == True:
            self.gravity += gravity # on accumule de la velocity grace a cette ligne
        self.y -= self.gravity

    #pas de saut infini  +  saut
    def sauter (self):
        if self.jump == True: # inverse la gravite + fait croire que le joueur n'est pas au sol donc la gravitee est activer
            return
        self.gravity = 12
        self.jump == True

    #affichage + animation
    def render (self):
        #saut gauche
        if self.jump == True and self.side_left == False:
            fenetre.blit(self.player_jump_right,(self.x,self.y))
        #saut droit
        elif self.jump == True and self.side_left == True:
            fenetre.blit(self.player_jump_left,(self.x,self.y))
        #marcher animation gauche
        elif self.side_left == True and self.move == True:
            if self.frame < 0: # tout les 6 frame on affiche un nouveau sprite
                self.frame = self.init_frame
                self.sprite += 1
                if self.sprite < 4:
                    fenetre.blit(self.ani_left[self.sprite],(self.x,self.y))
                else:
                    fenetre.blit(self.ani_left[self.sprite-1],(self.x,self.y))
                    self.sprite = 0
            else:
                fenetre.blit(self.ani_left[self.sprite],(self.x,self.y))
                self.frame -= 1
        #marcher animation droit
        elif self.side_left == False and self.move == True:
            if self.frame < 0:
                self.frame = self.init_frame
                self.sprite += 1
                if self.sprite < 4:
                    fenetre.blit(self.ani_right[self.sprite],(self.x,self.y))
                else:
                    fenetre.blit(self.ani_right[self.sprite-1],(self.x,self.y))
                    self.sprite = 0
            else:
                fenetre.blit(self.ani_right[self.sprite],(self.x,self.y))
                self.frame -= 1
        #position passive gauche
        elif self.side_left == True:
            fenetre.blit(self.player_left,(self.x,self.y))
            self.sprite = 0
            self.frame = self.init_frame
        #position passive droit
        elif self.side_left == False:
            fenetre.blit(self.player_right,(self.x,self.y))
            self.sprite = 0
            self.frame = self.init_frame
            
############################
#CHEAT

def cheat_engine(): # only presentation pas inclu en temps normal
    keys = pygame.key.get_pressed()

    if keys[pygame.K_p] and keys[pygame.K_RETURN]:
        presentation()
        
    if keys[pygame.K_o] and keys[pygame.K_RETURN]:
        money_add()

    if keys[pygame.K_i] and keys[pygame.K_RETURN]:
        ignore_event()
        
def presentation():
    global delay
    global event
    event = 10
    delay = 10

def money_add():
    global money
    money = money*2

def ignore_event():
    global fun
    global divise
    global double
    fun = 4
    divise = False
    double = False
#############################

#BASE DE DONNEE
    #menu
def reset(n):#reset le profil slectioner
    c.execute('DELETE FROM stuffToPlot WHERE nb_profil = ?',(n,))
    c.execute('CREATE TABLE IF NOT EXISTS stuffToPlot(nb_profil REAL, money REAL, player_power_up REAL, player_power_up_ REAL, npc_one REAL, npc_two REAL, npc_three REAL, npc_four REAL, npc_five REAL, npc_six REAL, npc_seven REAL, npc_height REAL)')
    c.execute("INSERT INTO stuffToPlot VALUES(?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)",(n,))
    conn.commit()

    
    #argent
def read_money(n):#lis l'argent du profil
    c.execute('SELECT money FROM stuffToPlot WHERE nb_profil=?',(n,))
    money = c.fetchone()
    return money

def update_money(money,profil):#enregistre l'argent sur le profil
    c.execute('UPDATE stuffToPlot SET money  = ? WHERE nb_profil = ?',(money,profil,))
    conn.commit()

    
    #LES AMELIORATIONS
def read_player(n):#lire les amelioration du profil selectionner
    c.execute('SELECT player_power_up,player_power_up_ FROM stuffToPlot WHERE nb_profil=?',(n,))
    powerup = c.fetchone()
    return powerup

def update_player_upgrade(n,profil):#amerlioration mineraux
    c.execute('UPDATE stuffToPlot SET player_power_up  = ? WHERE nb_profil = ?',(n,profil,))
    conn.commit()

def update_player_upgrade_(n,profil):#amelioration outil
    c.execute('UPDATE stuffToPlot SET player_power_up_  = ? WHERE nb_profil = ?',(n,profil,))
    conn.commit()

    
    #NPC
def read_npc(n):#lire tout les ouvrier du profil
    c.execute('SELECT npc_one, npc_two, npc_three, npc_four, npc_five, npc_six, npc_seven, npc_height FROM stuffToPlot WHERE nb_profil=?',(n,))
    npc = c.fetchone()
    return npc

def update_npc_one(n,profil):#grnad mere
    c.execute('UPDATE stuffToPlot SET npc_one  = ? WHERE nb_profil = ?',(n,profil,))
    conn.commit()

def update_npc_two(n,profil):#ami
    c.execute('UPDATE stuffToPlot SET npc_two  = ? WHERE nb_profil = ?',(n,profil,))
    conn.commit()

def update_npc_three(n,profil):#enfant fille
    c.execute('UPDATE stuffToPlot SET npc_three  = ? WHERE nb_profil = ?',(n,profil,))
    conn.commit()

def update_npc_four(n,profil):#enfant garcon
    c.execute('UPDATE stuffToPlot SET npc_four  = ? WHERE nb_profil = ?',(n,profil,))
    conn.commit()
    
def update_npc_five(n,profil):#immigre
    c.execute('UPDATE stuffToPlot SET npc_five  = ? WHERE nb_profil = ?',(n,profil,))
    conn.commit()

def update_npc_six(n,profil):#adulte
    c.execute('UPDATE stuffToPlot SET npc_six  = ? WHERE nb_profil = ?',(n,profil,))
    conn.commit()

def update_npc_seven(n,profil):#tech sous p
    c.execute('UPDATE stuffToPlot SET npc_seven  = ? WHERE nb_profil = ?',(n,profil,))
    conn.commit()

def update_npc_height(n,profil):#engeinier
    c.execute('UPDATE stuffToPlot SET npc_height  = ? WHERE nb_profil = ?',(n,profil,))
    conn.commit()


#pause fonction
def unpause():#elever la pause
    
    global pause
    pygame.mouse.set_visible(False)
    pause = False
    time.sleep(0.1)

def paused ():#fenetre de pause
    global event
    time.sleep(0.1)#importation + affichage (only 1 fois car sinon le fond n'est pas transparant
    IMGpause = pygame.image.load("image/game/pause.png").convert_alpha()
    resume = pygame.image.load("image/game/resume.png").convert_alpha()
    menu = pygame.image.load("image/game/menu.png").convert_alpha()
    qquit = pygame.image.load("image/game/quit.png").convert_alpha()
    
    fenetre.blit(IMGpause,(0,0))
    fenetre.blit(resume, (207,100))
    fenetre.blit(menu, (207,250))
    fenetre.blit(qquit, (207,400))

    while pause:#boucle infinie de la pause
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed() #input du user
    #Cursor
        mouse = pygame.mouse.get_pos()
        pygame.mouse.set_visible(True)

        if 207+362 > mouse[0] > 207 and 100+112 > mouse[1] >100:
            if pygame.mouse.get_pressed() == (1,0,0):#resume
                    unpause()
                                
        if 207+362 > mouse[0] > 207 and 250+112 > mouse[1] >250:
            if pygame.mouse.get_pressed() == (1,0,0):#retour menu
                    global minewin
                    minewin = False

                    global gamewin
                    gamewin = False
                    
                    unpause()
                    time.sleep(0.1)
                        

                                
        if 207+362 > mouse[0] > 207 and 400+112 > mouse [1] >400:
            if pygame.mouse.get_pressed() == (1,0,0):#quitter
                    pygame.mixer.music.stop()
                    pygame.quit()
                    quit()

        if keys[pygame.K_ESCAPE]:
            unpause()

        pygame.display.update()#maj de l'ecran
        clock.tick(60)
    


#fonction d'affichage des magazins d'amelioration
def upgrade(xori,yori,nom_1,icone_1,nom_2,icone_2,nom_3,icone_3,nom_4,icone_4,nom_5,icone_5,nom_6,icone_6,nom_7,icone_7,nom_8,icone_8,p):

    global money#import des global
    global mouse
    global click
    global profil
    global event
    
    nb_upgrade = read_player(profil)# choix de outil ou mineraux
    if p == 0 :
        n = int(nb_upgrade[0])
    elif p == 1 :
        n = int(nb_upgrade[1])
        
    price = (100,1000,10000,50000,100000,500000,1000000,5000000,0)#les prix en tuple

    text = 'Vous doublez votre production a la mine' #def texte dynamique ou pas
    achat_txt = font.render("Achat",9,yellow)
    prix_txt = font.render("Prix =",9,yellow)
    montant = font.render(str(price[n]),9,yellow)
    nb = font_petit.render(str(n),9,black)
    fin_txt = font_grand.render("Rupture de stock",9,red)
    fintxt = font_grand.render("Des outils",9,red)
    owned = font_petit.render("Numero de l'amerlioration posseder =",9,blue)
    mps_txt = font_petit.render(text,9,blue)

    pygame.mouse.set_visible(True) #affichage uu curseur
    
    if n < 8:#si nb de amelioration de l'amelioration choisie > 8
        if xori+470 < mouse[0] < xori+600 and yori+logo_y+115 < mouse[1] < yori+logo_y+150:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and click == True: 
                    if price[n] <= money:#achat
                        click = False
                        money = money - price[n]
                        n = n + 1
                        if p == 0 :#maj de la db
                            update_player_upgrade(n,profil)
                        elif p == 1:
                            update_player_upgrade_(n,profil)
                    elif price[n] > money:#acaht impossible
                        click = False
            else:
                click = True

#click == securite pour eviter le spam click

    #affichage des truc en fct de l'origine (haut-gauche du carre gris)
    fenetre.blit(fond,(xori,logo_y + yori))


    #Si l'achat est possible le bouton est vert
    if price[n] <= money:
            achat_txt = font.render("Achat",9,green)

    #Si l'achat est impossible le bouton est rouge
    if price[n] > money:
            achat_txt = font.render("Achat",9,red)

    #Dfinition des images interactife en focntion de la position de l'origine
        
    if n == 0:
        fenetre.blit(icone_1,(xori,logo_y+yori+30))
        fenetre.blit(nom_1,(xori+130,yori+logo_y+35))
        fenetre.blit(achat_txt,(xori+460,logo_y+yori+110))
        fenetre.blit(prix_txt,(xori+2,yori+logo_y-4))
        fenetre.blit(montant,(xori+135,yori+logo_y-4))
        fenetre.blit(owned,(xori+130,yori+logo_y+80))
        fenetre.blit(nb,(xori+450,yori+logo_y+80))
        fenetre.blit(mps_txt,(xori+130,yori+logo_y+110))
    if n == 1:
        fenetre.blit(icone_2,(xori,logo_y+yori+30))
        fenetre.blit(nom_2,(xori+130,yori+logo_y+35))
        fenetre.blit(achat_txt,(xori+460,logo_y+yori+110))
        fenetre.blit(prix_txt,(xori+2,yori+logo_y-4))
        fenetre.blit(montant,(xori+135,yori+logo_y-4))
        fenetre.blit(owned,(xori+130,yori+logo_y+80))
        fenetre.blit(nb,(xori+450,yori+logo_y+80))
        fenetre.blit(mps_txt,(xori+130,yori+logo_y+110))
    if n == 2:
        fenetre.blit(icone_3,(xori,logo_y+yori+30))
        fenetre.blit(nom_3,(xori+130,yori+logo_y+35))
        fenetre.blit(achat_txt,(xori+460,logo_y+yori+110))
        fenetre.blit(prix_txt,(xori+2,yori+logo_y-4))
        fenetre.blit(montant,(xori+135,yori+logo_y-4))
        fenetre.blit(owned,(xori+130,yori+logo_y+80))
        fenetre.blit(nb,(xori+450,yori+logo_y+80))
        fenetre.blit(mps_txt,(xori+130,yori+logo_y+110))
    if n == 3:
        fenetre.blit(icone_4,(xori,logo_y+yori+30))
        fenetre.blit(nom_4,(xori+130,yori+logo_y+35))
        fenetre.blit(achat_txt,(xori+460,logo_y+yori+110))
        fenetre.blit(prix_txt,(xori+2,yori+logo_y-4))
        fenetre.blit(montant,(xori+135,yori+logo_y-4))
        fenetre.blit(owned,(xori+130,yori+logo_y+80))
        fenetre.blit(nb,(xori+450,yori+logo_y+80))
        fenetre.blit(mps_txt,(xori+130,yori+logo_y+110))
    if n == 4:
        fenetre.blit(icone_5,(xori,logo_y+yori+30))
        fenetre.blit(nom_5,(xori+130,yori+logo_y+35))
        fenetre.blit(achat_txt,(xori+460,logo_y+yori+110))
        fenetre.blit(prix_txt,(xori+2,yori+logo_y-4))
        fenetre.blit(montant,(xori+135,yori+logo_y-4))
        fenetre.blit(owned,(xori+130,yori+logo_y+80))
        fenetre.blit(nb,(xori+450,yori+logo_y+80))
        fenetre.blit(mps_txt,(xori+130,yori+logo_y+110))
    if n == 5:
        fenetre.blit(icone_6,(xori,logo_y+yori+30))
        fenetre.blit(nom_6,(xori+130,yori+logo_y+35))
        fenetre.blit(achat_txt,(xori+460,logo_y+yori+110))
        fenetre.blit(prix_txt,(xori+2,yori+logo_y-4))
        fenetre.blit(montant,(xori+135,yori+logo_y-4))
        fenetre.blit(owned,(xori+130,yori+logo_y+80))
        fenetre.blit(nb,(xori+450,yori+logo_y+80))
        fenetre.blit(mps_txt,(xori+130,yori+logo_y+110))
    if n == 6:
        fenetre.blit(icone_7,(xori,logo_y+yori+30))
        fenetre.blit(nom_7,(xori+130,yori+logo_y+35))
        fenetre.blit(achat_txt,(xori+460,logo_y+yori+110))
        fenetre.blit(prix_txt,(xori+2,yori+logo_y-4))
        fenetre.blit(montant,(xori+135,yori+logo_y-4))
        fenetre.blit(owned,(xori+130,yori+logo_y+80))
        fenetre.blit(nb,(xori+450,yori+logo_y+80))
        fenetre.blit(mps_txt,(xori+130,yori+logo_y+110))
    if n == 7:
        fenetre.blit(icone_8,(xori,logo_y+yori+30))
        fenetre.blit(nom_8,(xori+130,yori+logo_y+35))
        fenetre.blit(achat_txt,(xori+460,logo_y+yori+110))
        fenetre.blit(prix_txt,(xori+2,yori+logo_y-4))
        fenetre.blit(montant,(xori+135,yori+logo_y-4))
        fenetre.blit(owned,(xori+130,yori+logo_y+80))
        fenetre.blit(nb,(xori+450,yori+logo_y+80))
        fenetre.blit(mps_txt,(xori+130,yori+logo_y+110))
    if n == 8:
        fenetre.blit(fin_txt,(xori+200,yori+logo_y+30))#out of stock
        fenetre.blit(fintxt,(xori+240,yori+logo_y+70))

#Définition des magazins de ouvrier
def prix(xori,yori,p,nom,icone,n):

    global money#import du global
    global mouse
    global profil
    global click
    global event

    nb_npc = read_npc(profil)#lecture des ouvrier deja acheter
    amount = (2,10,80,470,2600,14000,78000,440000)#ce qu'il raporte
    price = int(p*1.15**nb_npc[n])#pric en fonction de n (nb de ouvrier achete)
    pygame.mouse.set_visible(True)
    
    if xori+470 < mouse[0] < xori+600 and yori+logo_y+115 < mouse[1] < yori+logo_y+150:
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and click == True: 
                if price <= money:#achat
                    click = False#eviter le spam
                    money = money - price#maj de l'argent
                    npc_nb = nb_npc[n]#selection du ouvrier en qst
                    npc_nb += 1#maj des ouvriers
                    
                    if n == 0 : # maj de db
                        update_npc_one(npc_nb,profil)
                        
                    elif n == 1 :
                        update_npc_two(npc_nb,profil)
                        
                    elif n == 2 :
                        update_npc_three(npc_nb,profil)
                        
                    elif n == 3 :
                        update_npc_four(npc_nb,profil)
                        
                    elif n == 4 :
                        update_npc_five(npc_nb,profil)
                        
                    elif n == 5 :
                        update_npc_six(npc_nb,profil)
                        
                    elif n == 6 :
                        update_npc_seven(npc_nb,profil)
                        
                    elif n == 7 :
                        update_npc_height(npc_nb,profil)

                elif price > money:
                    click = False
        else:
            click = True

    #affichage des truc en fct de l'origine (haut-gauche du carre gris)
    fenetre.blit(fond,(xori,logo_y + yori))

    #Si l'achat est possible le bouton est vert
    if price <= money:
            achat_txt = font.render("Achat",9,green)

    #Si l'achat est impossible le bouton est rouge
    if price > money:
            achat_txt = font.render("Achat",9,red)
        

    #Permet de faire apparaitre du texte sur la fenetre pygame et des iamge
    prix_txt = font.render("Prix =",9,yellow)
    fenetre.blit(prix_txt,(xori+2,yori+logo_y-4))
    
    montant = font.render(str(price),9,yellow)
    fenetre.blit(montant,(xori+135,yori+logo_y-4))

    owned = font_petit.render('Possession =',9,blue)
    fenetre.blit(owned,(xori+130,yori+logo_y+80))
    
    nb = font_petit.render(str(int(nb_npc[n])),9,black)
    fenetre.blit(nb,(xori+245,yori+logo_y+80))

    mps_txt = font_petit.render('MPS =',9,blue)
    fenetre.blit(mps_txt,(xori+130,yori+logo_y+110))

    mps = font_petit.render(str(amount[n]),9,black)
    fenetre.blit(mps,(xori+185,yori+logo_y+110))

    fenetre.blit(icone,(xori+30,logo_y+yori+30))
    
    name = font_grand.render(nom,9,white)
    fenetre.blit(name,(xori+130,yori+logo_y+35))

    fenetre.blit(achat_txt,(xori+460,logo_y+yori+110))

    #Permet l'affichage du total d'argent dispo dans la boutique
def affichage_money_shop(money):

    money_txt = font.render('Minerais =',9,yellow)
    fenetre.blit(money_txt,(10,560))
    score_points = font.render(str(int(money)),9,yellow)
    fenetre.blit(score_points,(223,560))



    #Permet le changement de magazins depuis un magazins
def switchshop():
    
    global win_taverne#import des valeurs qui def les boucle inf des fenetres des magazins
    global win_home
    global win_black
    global win_tool
    global win_pole
    global event
    global click

    
    #import des imgs
    poleemploi = pygame.image.load("image/magazin/pole_icon.png").convert_alpha()
    blackmarket = pygame.image.load("image/magazin/black_icon.png").convert_alpha()
    house = pygame.image.load("image/magazin/home_icon.png").convert_alpha()
    tavernee = pygame.image.load("image/magazin/taverne_icon.png").convert_alpha()
    toul = pygame.image.load("image/magazin/tool_icon.png").convert_alpha()

#Zone de clique
    if 50 < mouse[0] < 50 +100 and 15 < mouse[1] < 15 + 50:
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and click == True:#ouvre le magazins de la maison et ferme les autres
                time.sleep(0.1)
                win_tool = False
                win_black = False
                win_pole = False
                win_taverne = False
                click = False
                home()
        else:
                click = True
            
    if 200 < mouse[0] < 200 + 100 and 15 < mouse[1] < 15  + 50:
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and click == True:#ouvre le magazins de la taverne et ferme les autres
                time.sleep(0.1)
                win_tool = False
                win_black = False
                win_pole = False
                win_home = False
                click = False
                taverne()
        else:
                click = True

    if 360 < mouse[0] < 360 + 100 and 15 < mouse[1] < 15 + 50:
        if event.type == MOUSEBUTTONDOWN:
            if event.button ==1 and click == True:#ouvre le magazins des ameliorations et ferme les autres
                time.sleep(0.1)
                win_black = False
                win_pole = False
                win_taverne = False
                win_home = False
                click = False
                tool()
        else:
                click = True

    if 500 < mouse[0] < 500 +100 and 15 < mouse[1] < 15 + 50:
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and click == True:#ouvre le magazins de pole emploi et ferme les autres
                time.sleep(0.1)
                win_tool = False
                win_black = False
                win_taverne = False
                win_home = False
                click = False
                pole()
        else:
                click = True

    if 650 < mouse[0] < 650 + 100 and 15 < mouse[1] < 15  + 50:
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and click == True:#ouvre le magazins du marche noir et ferme les autres
                time.sleep(0.1)
                win_tool = False
                win_pole = False
                win_taverne = False
                win_home = False
                click = False
                noir()
        else:
                click = True
            
    #affichage
    fenetre.blit(house,(50,logo_y-85))
    fenetre.blit(tavernee,(200,logo_y-85))
    fenetre.blit(toul,(360,logo_y-85))
    fenetre.blit(poleemploi,(500,logo_y-85))
    fenetre.blit(blackmarket,(650,logo_y-85))


def home():
# tout les magazins sont sur la meme base 
    time.sleep(0.1)#pause pour eviter le crashe du au event ca arrive mem avec la securiter pygame gere mal les evenement
    global money# imprt global
    global profil
    global mouse
    global event
    global win_home
    win_home = True# var de la boucle inf de la fenetre
    switch = False#eviter le spam de la fct switchshop
    
    mouse = pygame.mouse.get_pos() #def de la pos de la souris

#def des images
    perso1 = pygame.image.load("image/personnage/grandmere.png").convert_alpha()
    perso2 = pygame.image.load("image/personnage/ami.png").convert_alpha()
    fond = pygame.image.load("image/magazin/fond_shop.png").convert_alpha()
    logo = pygame.image.load("image/magazin/logo_home.png").convert_alpha()

    
    while win_home:#boucle inf pour la fenetre
        for event in pygame.event.get():# on fait defiler tous les evnements qui peuvent arriver au joueur
            if event.type == pygame.QUIT:# quitter avec la croix rouge
                pygame.mixer.music.stop()
                update_money(money,profil)#base de donnee
                win_home = False
                pygame.quit()
                quit()
                        
        money = cps(money) #maj de l'argent 
        mouse = pygame.mouse.get_pos()    # position de la souris
        #affichage du fond
        fenetre.blit(fond,(0,0)) 
        # logo
        fenetre.blit(logo,(400-170,115))
        #affichage du changement de magazin
        if switch == True:
            switchshop()
        #affihcage de l'agent
        affichage_money_shop(money)
        # utilisation des fonct pour afficher les elements interactif pour l'achat 
        prix(100,125,15,"Ta Grand Mere",perso1,0)
        prix(100,300,100,"Ton ami",perso2,1)

        affichage_event()#pour faire 
        
        switch = True

        ##back
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            win_home = False
            time.sleep(0.1)
            
        fenetre.blit(back,(25,115))
        if 25+47 > mouse[0] > 25 and 115+26 > mouse[1] >115:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    win_home = False
                    time.sleep(0.1)
                    
        pygame.display.update()
        clock.tick(60)
        
def taverne():

    time.sleep(0.1)
    global money
    global profil
    global mouse
    global event
    global win_taverne
    win_taverne = True
    switch = False
    
    mouse = pygame.mouse.get_pos()
    #Définition de chaque éléments

    perso1 = pygame.image.load("image/personnage/immigre.png").convert_alpha()
    perso2 = pygame.image.load("image/personnage/adulte.png").convert_alpha()
    fond = pygame.image.load("image/magazin/fond_shop.png").convert_alpha()
    logo = pygame.image.load("image/magazin/logo_taverne.png").convert_alpha()


    
    while win_taverne:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                update_money(money,profil)#base de donnee
                win_taverne = False
                pygame.quit()
                quit()
                
        money = cps(money)
        mouse = pygame.mouse.get_pos()    # position de la souris

        fenetre.blit(fond,(0,0)) #var (image , (position X, Position Y))
        
        fenetre.blit(logo,(400-170,115))
        #resolution de l'image en X et Y        X = 568  Y = 198
        #emplacement de l'image en X et Y       X = 96   Y = 56
        if switch == True:
            switchshop()
        affichage_money_shop(money)
        prix(100,125,130000,"Immigre",perso1,4)
        prix(100,300,1400000,"Adulte",perso2,5)

        affichage_event()
        
        switch = True
        
        ##back
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            win_taverne = False
            time.sleep(0.1)
            
        fenetre.blit(back,(25,115))
        if 25+47 > mouse[0] > 25 and 115+26 > mouse[1] >115:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    win_taverne = False
                    time.sleep(0.1)
                    
        pygame.display.update()
        clock.tick(60)

def tool():

    time.sleep(0.1)
    global money
    global profil
    global mouse
    global event
    global win_tool
    win_tool = True
    switch = False
    
    mouse = pygame.mouse.get_pos()
    #Définition de chaque éléments

    fond = pygame.image.load("image/magazin/fond_shop.png").convert_alpha()
    logo = pygame.image.load("image/magazin/logo_tool.png").convert_alpha()

    #def var mineraux
    txt_mineraux1 = font_grand.render('Charbon',9,white)
    txt_mineraux2 = font_grand.render('Bronze',9,white)
    txt_mineraux3 = font_grand.render('Fer',9,white)
    txt_mineraux4 = font_grand.render('Argent',9,white)
    txt_mineraux5 = font_grand.render('Or',9,white)
    txt_mineraux6 = font_grand.render('Platine',9,white)
    txt_mineraux7 = font_grand.render('Diamand',9,white)
    txt_mineraux8 = font_grand.render('Lythume',9,white)

    icon_mineraux1 = pygame.image.load('image/icon/charbon.png').convert_alpha()
    icon_mineraux2 = pygame.image.load('image/icon/cuivre.png').convert_alpha()
    icon_mineraux3 = pygame.image.load('image/icon/fer.png').convert_alpha()
    icon_mineraux4 = pygame.image.load('image/icon/argent.png').convert_alpha()
    icon_mineraux5 = pygame.image.load('image/icon/or.png').convert_alpha()
    icon_mineraux6 = pygame.image.load('image/icon/platine.png').convert_alpha()
    icon_mineraux7 = pygame.image.load('image/icon/diamand.png').convert_alpha()
    icon_mineraux8 = pygame.image.load('image/icon/lithum.png').convert_alpha()

    #def var outils
    txt_outils1 = font_grand.render('Truelle',9,white)
    txt_outils2 = font_grand.render('Pelle',9,white)
    txt_outils3 = font_grand.render('Pioche',9,white)
    txt_outils4 = font_grand.render('Pioche +',9,white)
    txt_outils5 = font_grand.render('Marteau Piqueur',9,white)
    txt_outils6 = font_grand.render('Marteau Piqueur +',9,white)
    txt_outils7 = font_grand.render('Pelleteuse',9,white)
    txt_outils8 = font_grand.render('Bagger 288',9,white)

    icon_outils1 = pygame.image.load('image/icon/truelle.png').convert_alpha()
    icon_outils2 = pygame.image.load('image/icon/pelle.png').convert_alpha()
    icon_outils3 = pygame.image.load('image/icon/pioche.png').convert_alpha()
    icon_outils4 = pygame.image.load('image/icon/pioche+.png').convert_alpha()
    icon_outils5 = pygame.image.load('image/icon/marteaupiqeur.png').convert_alpha()
    icon_outils6 = pygame.image.load('image/icon/marteaupiqeur+.png').convert_alpha()
    icon_outils7 = pygame.image.load('image/icon/pelleteuse.png').convert_alpha()
    icon_outils8 = pygame.image.load('image/icon/bagger288.png').convert_alpha()



    while win_tool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                update_money(money,profil)#base de donnee
                win_tool = False
                pygame.quit()
                quit()

        money = cps(money)
        mouse = pygame.mouse.get_pos()    # position de la souris

        fenetre.blit(fond,(0,0)) #var (image , (position X, Position Y))
        
        fenetre.blit(logo,(400-170,115))
        #resolution de l'image en X et Y        X = 568  Y = 198
        #emplacement de l'image en X et Y       X = 96   Y = 56

        if switch == True:
            switchshop()
        affichage_money_shop(money)
        upgrade(100,125,txt_mineraux1,icon_mineraux1,
                                txt_mineraux2,icon_mineraux2,
                                txt_mineraux3,icon_mineraux3,
                                txt_mineraux4,icon_mineraux4,
                                txt_mineraux5,icon_mineraux5,
                                txt_mineraux6,icon_mineraux6,
                                txt_mineraux7,icon_mineraux7,
                                txt_mineraux8,icon_mineraux8,0)
        
        upgrade(100,300,txt_outils1,icon_outils1,
                                txt_outils2,icon_outils2,
                                txt_outils3,icon_outils3,
                                txt_outils4,icon_outils4,
                                txt_outils5,icon_outils5,
                                txt_outils6,icon_outils6,
                                txt_outils7,icon_outils7,
                                txt_outils8,icon_outils8,1)

        affichage_event()

        switch = True
        
        ##back
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            win_tool = False
            time.sleep(0.1)
            
        fenetre.blit(back,(25,115))
        if 25+47 > mouse[0] > 25 and 115+26 > mouse[1] >115:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    win_tool = False
                    time.sleep(0.1)
        
                    
        pygame.display.update()
        clock.tick(60)


def pole():

    time.sleep(0.1)
    global money
    global profil
    global mouse
    global event
    global win_pole
    win_pole = True
    switch = False
    
    mouse = pygame.mouse.get_pos()
    #Définition de chaque éléments

    perso1 = pygame.image.load("image/personnage/tech.png").convert_alpha()
    perso2 = pygame.image.load("image/personnage/engenier.png").convert_alpha()
    fond = pygame.image.load("image/magazin/fond_shop.png").convert_alpha()
    logo = pygame.image.load("image/magazin/logo_pole.png").convert_alpha()


    
    while win_pole:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                update_money(money,profil)#base de donnee
                win_pole = False
                pygame.quit()
                quit()
                
        money = cps(money)
        mouse = pygame.mouse.get_pos()    # position de la souris

        fenetre.blit(fond,(0,0)) #var (image , (position X, Position Y))
        
        fenetre.blit(logo,(400-170,115))
        #resolution de l'image en X et Y        X = 568  Y = 198
        #emplacement de l'image en X et Y       X = 96   Y = 56

        if switch == True:
            switchshop()
        affichage_money_shop(money)
        prix(100,125,20000000,"Technicien sous paye",perso1,6)
        prix(100,300,330000000,"Ingenieur",perso2,7)

        affichage_event()
        
        switch = True
        
        ##back
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            win_pole = False
            time.sleep(0.1)
            
        fenetre.blit(back,(25,115))
        if 25+47 > mouse[0] > 25 and 115+26 > mouse[1] >115:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    win_pole = False
                    time.sleep(0.1)
                    
        pygame.display.update()
        clock.tick(60)

def noir():

    time.sleep(0.1)
    global money
    global profil
    global mouse
    global event
    global win_black
    win_black = True
    switch = False
    
    mouse = pygame.mouse.get_pos()
    #Définition de chaque éléments

    perso1 = pygame.image.load("image/personnage/enfantfille.png").convert_alpha()
    perso2 = pygame.image.load("image/personnage/enfantgarcon.png").convert_alpha()
    fond = pygame.image.load("image/magazin/fond_shop.png").convert_alpha()
    logo = pygame.image.load("image/magazin/logo_black.png").convert_alpha()

    
    while win_black:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                update_money(money,profil)#base de donnee
                win_black = False
                pygame.quit()
                quit()
                
        money = cps(money)
        mouse = pygame.mouse.get_pos()    # position de la souris

        fenetre.blit(fond,(0,0)) #var (image , (position X, Position Y))
        
        fenetre.blit(logo,(400-170,115))
        #resolution de l'image en X et Y        X = 568  Y = 198
        #emplacement de l'image en X et Y       X = 96   Y = 56

        if switch == True:
            switchshop()
        affichage_money_shop(money)

        prix(100,125,1100,"Enfant Fille",perso1,2)
        prix(100,300,12000,"Enfant Garcon",perso2,3)

        affichage_event()
        
        switch = True
        
        ##back
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            win_black = False
            time.sleep(0.1)
            
        fenetre.blit(back,(25,115))
        if 25+47 > mouse[0] > 25 and 115+26 > mouse[1] >115:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    win_black = False
                    time.sleep(0.1)
        
            
        pygame.display.update()
        clock.tick(60)

def game():
    
    time.sleep(0.1)
    global profil
    global gamewin
    global pause
    global event
    global money
    gamewin = True
    Xpos = 0 #world
    Ypos = 0
    XXpos = 100
    YYpos = 500
    POSx_r = 100
    centre = True
    left = False
    right = False
    move_left_pos = False
    move_rgiht_pos = False
    vitesse = 8
    
    #valeur du player avec les classes
    gravity = -1
    movex = 0
    movey = 0
    player = Player(XXpos,YYpos)#cordo du spawn
    ###
    
    IMGbg = pygame.image.load("image/game/gamebackground.png").convert_alpha()
    grasse = pygame.image.load("image/game/grasse.png").convert_alpha()
    popup = pygame.image.load('image/game/popup.png').convert_alpha()

    money = read_money(profil)#base de donnee
    money = money[0]
    
    while gamewin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                update_money(money,profil)#base de donnee
                gamewin = False
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
    #pause
        if keys[pygame.K_ESCAPE]:
                update_money(money,profil)#base de donnee
                pause = True
                paused()
    #mouvement
        #left move
        if -10 < Xpos:
            if keys[pygame.K_RIGHT] and centre == True:
                Xpos += -vitesse
                left = False
                POSx_r += vitesse
                
                
            elif keys[pygame.K_RIGHT] and centre == False:
                player.x += vitesse
                left = True
                POSx_r += vitesse

            if player.x > 0:
                if keys[pygame.K_LEFT]:
                    player.x += -vitesse
                    POSx_r += -vitesse
        else:
            if keys[pygame.K_LEFT] and right == False:
                Xpos += vitesse
                POSx_r += -vitesse

        #right move
        if Xpos < -1100:
            if keys[pygame.K_LEFT] and centre == True:
                Xpos += vitesse
                right = False
                POSx_r += -vitesse
                
            elif keys[pygame.K_LEFT] and centre == False:
                right = True
                player.x += -vitesse
                POSx_r += -vitesse
                
            if player.x < 750:
                if keys[pygame.K_RIGHT]:
                    player.x += vitesse
                    POSx_r += vitesse
                    
        else:
            if keys[pygame.K_RIGHT] and left == False:
                Xpos += -vitesse
                POSx_r += vitesse
        #jump
        if keys[pygame.K_SPACE]:

            player.sauter()
            
        #check player centre  
        if 390 < player.x < 410:
            centre = True
        else:
            centre = False

        #check side
        if player.x < 390:
            left = True
        elif player.x > 410:
            right =True
            
        #aniamtion
        if keys[pygame.K_RIGHT]:
            player.side_left = True
            player.move = True
            
        elif keys[pygame.K_LEFT]:
            player.side_left = False
            player.move = True
            
        else:
            player.move = False
        
        
        fenetre.blit(IMGbg,(Xpos,Ypos))
    #lieux
        #HOME
        if 0 < POSx_r < 200 :
            fenetre.blit(popup,(player.x-55,player.y-70))
            if keys[pygame.K_UP]:
                home()
                time.sleep(0.1)
        #TAVERNE
        if 476 < POSx_r < 715 :
            fenetre.blit(popup,(player.x-55,player.y-70))
            if keys[pygame.K_UP]:
                taverne()
                time.sleep(0.1)
        #SHOP
        if 996 < POSx_r < 1105 :
            fenetre.blit(popup,(player.x-55,player.y-70))
            if keys[pygame.K_UP]:
                tool()
                time.sleep(0.1)
        #POLE EMPOIS
        if 1244< POSx_r < 1340 :
            fenetre.blit(popup,(player.x-55,player.y-70))
            if keys[pygame.K_UP]:
                pole()
                time.sleep(0.1)
        #MN
        if 1580 < POSx_r < 1685 :
            fenetre.blit(popup,(player.x-55,player.y-70))
            if keys[pygame.K_UP]:
                noir()
                time.sleep(0.1)
        #MINE
        if 1765 < POSx_r < 1920 :
            fenetre.blit(popup,(player.x-55,player.y-70))
            if keys[pygame.K_UP]:
                mine()
                time.sleep(0.1)
        
        ## utilisation de classe
        player.ground()
        player.update(gravity)
        player.render()
        ###
        
        fenetre.blit(grasse,(Xpos,582))
        
        money = cps(money)
        affichage_money(money)
        affichage_event()

        ###HACKS!!!
        cheat_engine()

        
        pygame.display.flip()
        clock.tick(60)
        
#money

def affichage_money(money):

    money_txt = font.render('Minerais =',9,yellow)
    fenetre.blit(money_txt,(10,10))
    score_points = font.render(str(int(money)),9,yellow)
    fenetre.blit(score_points,(223,10))
    
#cps
    
def cps(money):
        global profil
        
        money = game_event(money) #cata et subvention
        amount = (2,10,80,470,2600,14000,78000,440000)
        npc = read_npc(profil)
        cps = 0
        for n in range (8):
                cps += npc[n]*amount[n]
        cps = famine(cps)
        cps = faillite(cps)
        money += cps/60
        
        return money

#EVENEMENTS
def subvention(money):
    
    gain = money * 0.1
    money += gain

    return money

def cataclysme(money):
    
    gain = money * 0.1
    money -= gain

    return money

def faillite(cps):
    global delay
    global double
    
    if delay > 9000 and double == True:
        cps = cps*2
    else:
        double = False
        
    return cps

def famine(cps):
    global divise
    global delay
    if delay > 9000 and divise == True:
        cps =  cps/2
    else:
        divise = False
    return cps

#events

def game_event(money):
    global delay
    global fun
    global divise
    global double
    
    if delay == 0:
            fun = randint(0,3)
            if fun == 0:
                money = subvention(money)
            elif fun == 1:
                double = True
            elif fun == 2:
                divise = True
            elif fun == 3:
                money = cataclysme(money)
    
            delay = 10800
    else:
        if delay != 0:
            delay = delay - 1

    if delay < 10200:
        fun = 4
    
    return money

def affichage_event():
    global fun
    
    event_un = pygame.image.load("image/game/event1.png").convert_alpha()
    event_deux = pygame.image.load("image/game/event2.png").convert_alpha()
    event_trois = pygame.image.load("image/game/event3.png").convert_alpha()
    event_quatre = pygame.image.load("image/game/event4.png").convert_alpha()

    
    if fun == 0:
        fenetre.blit(event_un,(250,150))
        
    elif fun == 1:
        fenetre.blit(event_deux,(250,150))
        
    elif fun == 2:
        fenetre.blit(event_trois,(250,150))
        
    elif fun == 3:
        fenetre.blit(event_quatre,(250,150))

def CM_db(CM):
    global profil
    powerup = read_player(profil)
    CM = CM**(1+powerup[0]+powerup[1])
    return CM
    
#La mine
def mine ():

    global money
    global profil
    global minewin
    global pause
    
    push = True
    minewin = True
    pygame.mouse.set_visible(False)
    son = pygame.mixer.Sound("sound/clic.wav")
    clic = pygame.image.load("image/game/clic.png").convert_alpha()
    background_rock = pygame.image.load("image/game/background_rock.png").convert_alpha()
    cursor = pygame.image.load("image/game/pickaxe.png").convert_alpha()
    back = pygame.image.load("image/menu/back.png").convert_alpha()
    timer = 0
    
    while minewin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                update_money(money,profil)#base de donnee
                pygame.quit()
                quit()

        fenetre.blit(background_rock,(0,0))
        mouse = pygame.mouse.get_pos()
        fenetre.blit(cursor,mouse)
        CM = 2 #base
        CM = CM_db(CM)
        CM = famine(CM)
        CM = faillite(CM)
        CMtext = font.render(str(int(CM)),9,white)
        CMtextt = font.render(str(int(CM)),9,green)
        plus = font.render("+",6,white)
        pluss = font.render("+",6,green)
        keys = pygame.key.get_pressed()
        affichage_money(money)
#back
        fenetre.blit(back, (25,565))
        if 25+47 > mouse[0] > 25 and 565+26 > mouse[1] >25:
            if pygame.mouse.get_pressed() == (1,0,0):
                update_money(money,profil)#base de donnee
                minewin = False
#retour
        if keys[pygame.K_ESCAPE]:
            minewin = False
            time.sleep(0.1)
#miner event
        if pygame.mouse.get_pressed() == (1,0,0) and push == True :
            son.play()
            push = False
            timer = 10
            pos = 1
            money += CM
            
        elif pygame.mouse.get_pressed() == (0,0,0):
            push = True
            
#affichage miner
        if timer > 2:
            fenetre.blit(clic,(mouse[0]-12,mouse[1]-15))
            
        if timer > 0:
            pos += 2
            timer -= 1
            fenetre.blit(plus,(mouse[0]+50+pos,mouse[1]+10+pos))
            fenetre.blit(CMtext,(mouse[0]+70+pos,mouse[1]+10+pos))
            fenetre.blit(pluss,(50+pos+150,30+(2*pos)))
            fenetre.blit(CMtextt,(70+pos+150,30+(2*pos)))

        money = cps(money)
        affichage_event()

        cheat_engine()

        pygame.display.update()
        clock.tick(60)




def menu_profile():
    
    global profil
    global event
    
    time.sleep(0.1)
    menu_profile = True
    #import      
    play_little_b = pygame.image.load("image/menu/play_little_b.png").convert_alpha()
    reset_little_b = pygame.image.load("image/menu/reset_little_b.png").convert_alpha()
    play_little = pygame.image.load("image/menu/play_little.png").convert_alpha()
    reset_little = pygame.image.load("image/menu/reset_little.png").convert_alpha()
    back = pygame.image.load("image/menu/back.png").convert_alpha()
    background_profile = pygame.image.load("image/menu/background_profile.png").convert_alpha()
    select_profile = pygame.image.load("image/menu/select_profile.png").convert_alpha()
    select_profile_b = pygame.image.load("image/menu/select_profile_b.png").convert_alpha()
    
    while menu_profile:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                quit()

    
        mouse = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
    #texte
        un = font.render('Profile 1',9,white)
        deux = font.render('Profile 2',9,white)
        trois = font.render('Profile 3',9,white)
        money_txt = font.render('Minerais =',9,yellow)

        money_un = read_money(1)#base de donnee
        money_deux = read_money(2)#base de donnee
        money_trois = read_money(3)#base de donnee

        txt_money_un = font.render(str(int(money_un[0])),9,green)
        txt_money_deux = font.render(str(int(money_deux[0])),9,green)
        txt_money_trois = font.render(str(int(money_trois[0])),9,green)
    
    #fond
        fenetre.blit(background_profile, (1,1))
        
    #affichage selection
        
        if profil == 1:
            fenetre.blit(select_profile_b, (176,64))
        else:
            fenetre.blit(select_profile, (176,64))

        
        if profil == 2:
            fenetre.blit(select_profile_b, (176,197))
        else:
            fenetre.blit(select_profile, (176,197))

        
        if profil == 3:
            fenetre.blit(select_profile_b, (176,329))
        else:
            fenetre.blit(select_profile, (176,329))

    #selection
            
        if 176+450 > mouse[0] > 176 and 64+125 > mouse[1] >64:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    profil = 1


        if 176+450 > mouse[0] > 176 and 197+125 > mouse[1] >197:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    profil = 2


        if 176+450 > mouse[0] > 176 and 329+125 > mouse[1] >329:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    profil = 3

    #option
        if 81+206 > mouse[0] > 81 and 504+64 > mouse[1] >504:
            fenetre.blit(play_little_b, (81,504))
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    game()
        else:
            fenetre.blit(play_little, (81,504))

        if 540+206 > mouse[0] > 540 and 504+64 > mouse[1] >504:
            fenetre.blit(reset_little_b, (540,504))
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    reset(profil)#base de donnee
        else:
            fenetre.blit(reset_little, (540,504))
    #back
        fenetre.blit(back, (25,25))
        if 25+47 > mouse[0] > 25 and 25+26 > mouse[1] >25:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    menu_profile = False

        if keys[pygame.K_ESCAPE]:
            menu_profile = False
            time.sleep(0.1)
                    
    #Affichage texte
        fenetre.blit(un, (176, 64))
        fenetre.blit(deux, (176, 197))
        fenetre.blit(trois, (176, 329))
        fenetre.blit(txt_money_un, (176+15+15,64+80))
        fenetre.blit(txt_money_deux, (176+15+15,197+80))
        fenetre.blit(txt_money_trois, (176+15+15,329+80))
        fenetre.blit(money_txt,(176+15,64+50))
        fenetre.blit(money_txt,(176+15,197+50))
        fenetre.blit(money_txt,(176+15,329+50))

    #Cursor
        pygame.mouse.set_visible(False)
        cursor = pygame.image.load("image/menu/cursor.png")
        fenetre.blit(cursor, (mouse[0],mouse[1]))
        
    #Fin
        pygame.display.update()
        clock.tick(60)
#Menu
def game_menu ():
    global event
    time.sleep(0.1)
    menu = True
    volume = float(0.1)
    pygame.mixer.music.set_volume(volume)

#Fond
    bg = pygame.image.load("image/menu/background.png").convert()

    
#Import
    play_b = pygame.image.load("image/menu/play_b.png").convert_alpha()
    qquit_b = pygame.image.load("image/menu/quit_b.png").convert_alpha()
    qquit = pygame.image.load("image/menu/quit.png").convert_alpha()
    play = pygame.image.load("image/menu/play.png").convert_alpha()
    volume_up = pygame.image.load("image/menu/volume_up.png").convert_alpha()
    volume_down = pygame.image.load("image/menu/volume_down.png").convert_alpha()
    cursor = pygame.image.load("image/menu/cursor.png").convert_alpha()
    logo = pygame.image.load("image/menu/logo.png").convert_alpha()
    
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                quit()
                
        mouse = pygame.mouse.get_pos()
        pcvolume = int(volume*100+0.01)
        txt_volume = font.render(str(pcvolume),9,yellow)
        pc = font.render('%',9,yellow)
        
        fenetre.blit(bg, (0,0))
        fenetre.blit(logo, (96,56))
        fenetre.blit(volume_down, (750,551))
        fenetre.blit(volume_up, (692,551))
        fenetre.blit(txt_volume,(700,520))
        fenetre.blit(pc,(765,520))
        pygame.mouse.set_visible(False)
        
        
        if 692+43 > mouse[0] > 692 and 551+39 > mouse[1] >551:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if volume < 0.99:
                        volume = volume + 0.01
                        volume = float(volume)
                        pygame.mixer.music.set_volume(volume)

        if 750+43 > mouse[0] > 750 and 551+39 > mouse[1] >551:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if volume > 0.01:
                        volume = volume - 0.01
                        volume = float(volume)
                        pygame.mixer.music.set_volume(volume)
    # Boutton selction
        if 207+362 > mouse[0] > 207 and 292+112 > mouse[1] >292:
            fenetre.blit(play_b, (207,292))
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    menu_profile()
        else:
            fenetre.blit(play, (207,292))

        if 207+362 > mouse[0] > 207 and 462+112 > mouse[1] >462:
            fenetre.blit(qquit_b, (207,462))
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    quit()
        else:
            fenetre.blit(qquit, (207,462))

        fenetre.blit(cursor,(mouse)) 
        pygame.display.update()
        clock.tick(60)

game_menu()
pygame.quit()
quit()
