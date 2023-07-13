import pygame as pg
from constantes_crisis import *

# Clase para representar una barra de salud
class health_bar():
    def __init__(self,x,y,health,max_health) -> None:
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
        
    def draw(self,health,screen):
        """dibuja  la barra de vida del jugador"""
        self.health = health
        ratio = self.health / self.max_health # Calcula la proporción de salud con respecto a la salud máxima
        pg.draw.rect(screen,(0,0,0),(self.x - 2,self.y -2 ,154,24))
        pg.draw.rect(screen,(255,0,0),(self.x,self.y,150,20))
        pg.draw.rect(screen, (0,255,0),(self.x,self.y,150 * ratio,20))