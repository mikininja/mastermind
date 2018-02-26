# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 18:16:34 2018

@author: miki1
"""

import pygame
from pygame.locals import Rect
from random import randint
from math import sqrt
pygame.font.init() 
myfont = pygame.font.SysFont('Comic Sans MS', 30)
myfont1 = pygame.font.SysFont('Comic Sans MS', 50)
L=1000
SIZEX=800
SIZEY=800
def getcol(n):
    if n==0:
        return (0,0,0)
    elif n==1:
        return (255,255,255)
    elif n==2:
        return (255,0,0)
    elif n==3:
        return (0,255,0)
    elif n==4:
        return (0,0,255)
    elif n==5:
        return (255,255,0)
def dist(p1,p2):
    return sqrt((p1.x-p2.x)**2+(p1.y-p2.y)**2)
class punto(object):
    def __init__(self,x,y,val):
        self.x=x
        self.y=y
        self.val=val
class piolo(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.col=-1
        self.visible=False
class Board(object):
    def __init__(self,sx,sy):
        self.x=sx
        self.y=sy
        pygame.init()
        self.rekt=Rect(0,0,sx,sy)
        self.screen=pygame.display.set_mode(self.rekt.size,0)
        self.bg=pygame.Surface(self.rekt.size)
        self.finito=False
        self.combinazione=[]
        self.turno=0
        self.matrice=[]
        self.scelta=-1
        self.pioli=[]
        self.arrayscelte=[(40,50),(100,50),(40,110),(100,110),(40,170),(100,170),(70,230)]
        voffset=120
        for i in range(9):
            ooffset=220
            self.matrice.append([])
            for j in range(4):
                self.matrice[i].append(punto(ooffset,voffset,-1))
                ooffset=ooffset+60
            voffset=voffset+70
        for i in range(4):
            self.combinazione.append(randint(0,5))
        voffset=105
        for i in range(9):
            ooffset=460
            self.pioli.append([])
            for j in range(2):
                self.pioli[i].append(piolo(ooffset,voffset))
                ooffset=ooffset+30
            voffset=voffset+30
            ooffset=460
            for j in range(2):
                self.pioli[i].append(piolo(ooffset,voffset))
                ooffset=ooffset+30
            voffset=voffset+40
    def onexit(self):
        pygame.time.delay(2000)
        #self._running = False
        #pygame.quit()
    def mostramat(self):
        for r in self.matrice:
            for p in r:
                if p.val==-1:
                    pygame.draw.circle(self.screen,(0,0,0),(p.x,p.y),20,1)
                else:
                    pygame.draw.circle(self.screen,getcol(p.val),(p.x,p.y),20)
    def disegnasol(self):
        offset=220
        for v in self.combinazione:
            pygame.draw.circle(self.screen,getcol(v),(offset,50),20)
            offset=offset+60
        if not self.finito:
            pygame.draw.rect(self.screen,(0,0,0),Rect(190,20,240,60))
    def disegnascelte(self):
        pygame.draw.circle(self.screen,getcol(0),(40,50),20)
        pygame.draw.circle(self.screen,getcol(1),(100,50),20)
        pygame.draw.circle(self.screen,getcol(2),(40,110),20)
        pygame.draw.circle(self.screen,getcol(3),(100,110),20)
        pygame.draw.circle(self.screen,getcol(4),(40,170),20)
        pygame.draw.circle(self.screen,getcol(5),(100,170),20)
        pygame.draw.circle(self.screen,getcol(1),(70,230),20)
        textsurface = myfont.render("C", False, (0,0,0))
        self.screen.blit(textsurface,(60,210))
    def checkifscelta(self,pos):
        for e in self.arrayscelte:
            if dist(punto(pos[0],pos[1],-1),punto(e[0],e[1],-1))<=20:
                ret=-1 if self.arrayscelte.index(e)==6 else self.arrayscelte.index(e)
                return ret
        return -2
    def printdifferences(self):
        for p in self.pioli[self.turno]:
            p.visible=True
        blacktoadd=0
        for i in range(4):
            if self.combinazione[i]==self.matrice[self.turno][i].val:
                blacktoadd=blacktoadd+1
        whitetoadd=0
        for i in range(blacktoadd):
            self.pioli[self.turno][i].col=0
        
        provafatta=[]
        for e in self.matrice[self.turno]:
            provafatta.append(e.val)
        for e in self.combinazione:
            if e in provafatta:
                whitetoadd=whitetoadd+1
                provafatta.remove(e)
        
        whitetoadd=whitetoadd-blacktoadd
        for i in range(blacktoadd,blacktoadd+whitetoadd):
            self.pioli[self.turno][i].col=1
        
    def printpioli(self):
        for r in self.pioli:
            for p in r:
                if p.visible==True:
                    if p.col==-1:
                        pygame.draw.circle(self.screen,(0,0,0),(p.x,p.y),10,1)
                    elif p.col==0:
                        pygame.draw.circle(self.screen,(0,0,0),(p.x,p.y),10)
                    elif p.col==1:
                        pygame.draw.circle(self.screen,(255,255,255),(p.x,p.y),10)
    def passaturno(self):
        count=0
        for e in self.matrice[self.turno]:
            if e.val==-1:
                count=count+1
        if count==0:
            self.printdifferences()
            self.turno=self.turno+1
            if self.turno>8:
                self.finito=True
                print("GAME OVER, hai perso")
                textsurface1 = myfont1.render("HAI PERSO!", False, (255,255,0))
                self.screen.blit(textsurface1,(100,400))
                pygame.display.update()
                self.onexit()
                
    def checkvictory(self):
        provafatta=[]
        for e in self.matrice[self.turno]:
            provafatta.append(e.val)
        if provafatta==self.combinazione:
            self.finito=True
            print("VITTORIA! Hai indovinato la combinazione segreta!!")
            textsurface1 = myfont1.render("HAI VINTO!", False, (255,255,0))
            self.screen.blit(textsurface1,(100,400))
            pygame.display.update()
            self.onexit()
        else:
            self.passaturno()
    def checkifdest(self,pos):
        for e in self.matrice[self.turno]:
            if dist(punto(pos[0],pos[1],-1),e)<=20:
                return self.matrice[self.turno].index(e)
        return -2
    def gestisciclick(self,pos):
        if self.checkifscelta(pos)!=-2:
            self.scelta=self.checkifscelta(pos)
        else:
            if self.checkifdest(pos)!=-2:
                self.matrice[self.turno][self.checkifdest(pos)].val=self.scelta
                self.mostramat()
                pygame.display.update()
                self.checkvictory()
            
    def disegnagriglia(self):
        for v in range(90,720,70):
            pygame.draw.rect(self.screen,(0,0,0),Rect(190,v,240,60),1)
    def blit(self):
        self.screen.fill((219,112,147))
        self.disegnasol()
        self.disegnascelte()
        self.disegnagriglia()
        self.mostramat()
        self.printpioli()
        pygame.display.update()
    
    def run(self):
        while 1:
            self.blit()
            #pygame.time.delay(5)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self._running = False
                    pygame.quit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    clicksu=pygame.mouse.get_pos()
                    self.gestisciclick(clicksu)
            

class Splash(object):
    def __init__(self):
        self.x=SIZEX
        self.y=SIZEY

if __name__=="__main__":

    game=Board(SIZEX,SIZEY)
    game.run()