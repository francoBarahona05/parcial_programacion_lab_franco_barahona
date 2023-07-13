from typing import Any
import pygame as pg
from constantes_crisis import *
from auxiliar import *
TITLE_SIZE = 40

class itemBox(pg.sprite.Sprite):
    def __init__(self, item_type,x, y) -> None:
       pg.sprite.Sprite.__init__(self)
       self.item_type = item_type
       self.image = item_boxes[self.item_type]
       self.rect = self.image.get_rect()
       self.rect.midtop = (x + TITLE_SIZE // 2 , y + (TITLE_SIZE - self.image.get_height()))
       
    def update(self,player,scroll,sound) -> None:
        self.rect.x += scroll
        if pg.sprite.collide_rect(self, player):
            sound.play()
            if self.item_type == "health":
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == "ammo":
                player.ammo += 10

            elif self.item_type == "granade":
                player.ammo_granade += 3

            self.kill()
       
       