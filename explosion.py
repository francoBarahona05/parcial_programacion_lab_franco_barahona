import pygame as pg
from constantes_crisis import *
from auxiliar import explosion 

class granade_explosion(pg.sprite.Sprite):
    def __init__(self, x, y,scale) -> None:
        """ Inicialización del sprite de explosión de granada"""
        pg.sprite.Sprite.__init__(self)
        self.images = []
        # Cargar las imágenes de la explosión
        for i in range(1,6):
            img = pg.image.load(f"img\\G.U.N SEPARADO POR NEO GYL\\explosion\\exp{i}.png")
            img = pg.transform.scale(img,(int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0 # Índice de cuadro actual
        self.image = self.images[self.frame_index] 
        self.rect = self.image.get_rect() # Rectángulo del sprite
        self.rect.center = (x,y)  # Coordenadas del centro del sprite
        self.counter = 0# Contador para controlar la animación
    
       
    def update(self):
        """encargado de animar la explosion"""
        EXPLOSION_SPEED = 1.3
        self.counter += 1
        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            granade_sound.play()
            
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index] # Actualizar la imagen actual