import pygame as pg
from constantes_crisis import *
from auxiliar import granade
from explosion import granade_explosion

class granades(pg.sprite.Sprite):
    def __init__(self, x, y, direction ) -> None:
       pg.sprite.Sprite.__init__(self)
       self.timer = 50
       self.vel_y = -11 # Velocidad vertical inicial
       self.speed = 15 # Velocidad horizontal
       self.image = granade
       self.image = pg.transform.scale(self.image,(int(self.image.get_width() + 14),(self.image.get_height() + 14)))
       self.rect = self.image.get_rect()
       self.rect.center = (x,y) # Coordenadas del centro del sprite
       self.direction = direction # Dirección (1 para derecha, -1 para izquierda)
       self.width = self.image.get_width() - 10
       self.height  = self.image.get_height() 
       
    def update(self , player_ , worlds,pan ,scroll):
        """ Actualizar la posición de la granada en función de la física del juego"""
        self.vel_y += GRAVITY + 2
        dx = self.direction * self.speed  # Cambio horizontal
        dy = self.vel_y # Cambio vertical
        pg.draw.rect(pan, (255, 0, 0), self.rect, 2)

        for tile in worlds.obstacle_list:
            # Comprobar colisiones con los obstáculos del mundo
            if tile[1].colliderect(self.rect.x + dx , self.rect.y , self.width,self.height):
                self.direction *= -1 # Cambiar la dirección al colisionar con un obstáculo
                dx = self.direction * self.speed
                
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width,self.height):
                self.speed = 0 # Detener la granada al colisionar verticalmente
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    self.jumping = False
                    dy = tile[1].top - self.rect.bottom

        self.rect.x += dx + scroll # Actualizar la posición horizontal
        self.rect.y += dy  # Actualizar la posición vertical
        
        if self.rect.left + dx  < 0 or self.rect.right + dx > ANCHO_PANTALLA:
            self.direction *= -1 # Cambiar la dirección al llegar a los límites de la pantalla
            dx = self.direction * self.speed
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion_granade = granade_explosion(self.rect.x,self.rect.y,0.5)            
            EXPLOSION_GROUP.add(explosion_granade)
            
            if abs(self.rect.centerx - player_.rect.centerx) < TITLE_SIZE * 2 and abs(self.rect.centerx - player_.rect.centerx) < TITLE_SIZE * 2 :
                player_.health -= 50 
                
            for enemy in ENEMY_GROUP:
                if abs(self.rect.centerx - enemy.rect.centerx) < TITLE_SIZE * 2 and abs(self.rect.centerx - enemy.rect.centerx) < TITLE_SIZE * 2 :
                    enemy.health -= 50 


        