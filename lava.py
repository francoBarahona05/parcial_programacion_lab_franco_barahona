import pygame as pg
from constantes_crisis  import *
# Clase para representar una plataforma de lava
class lava(pg.sprite.Sprite):
    def __init__(self, img , x , y) -> None:
        pg.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tile_size  // 2, y + (tile_size - self.image.get_height()))# Posición de la plataforma
        
    def update(self,scroll):
        self.rect.x += scroll # Actualiza la posición horizontal de la plataforma con el desplazamiento (scroll)
