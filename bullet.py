from typing import Any
import pygame as pg
from constantes_crisis import *

class bullets(pg.sprite.Sprite):
    def __init__(self, x, y, direction, image) -> None:
        # Constructor de la clase bullets
        pg.sprite.Sprite.__init__(self)
        self.speed = 18
        self.image = image
        # Escalar la imagen de la bala según la constante SCALE_BULLET
        self.image = pg.transform.scale(self.image, (int(self.image.get_width() * SCALE_BULLET), int(self.image.get_height() * SCALE_BULLET)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self) -> None:
        """ Actualizar la posición de la bala en cada fotograma"""
        self.rect.x += self.direction * self.speed
        # Eliminar la bala si sale de los límites de la pantalla
        if self.rect.right < 0 or self.rect.left > ANCHO_PANTALLA:
            self.kill()

    def check_collision(self, player, enemy, bullets, state=False):
        """ Comprobar colisiones de la bala con el jugador y los enemigos"""
        if pg.sprite.spritecollide(player, bullets, state):
            # Colisión con el jugador
            if player.alivee:
                player.health -= 5
                self.kill()
        if pg.sprite.spritecollide(enemy, bullets, state):
            # Colisión con el enemigo
            if enemy.alive:
                player.health -= 25
                self.kill()

# Comentarios explicativos
# - Importaciones de módulos
# - Definición de la clase bullets
# - Constructor de la clase
# - Método update
# - Método check_collision
