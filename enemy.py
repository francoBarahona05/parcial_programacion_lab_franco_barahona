import pygame as pg
from player import player_game  
from auxiliar import * 
from constantes_crisis import *  
import random

# Clase para representar a los enemigos
class enemys(player_game):

    def __init__(self, x, y, scale, speed, animation_speed):
        super().__init__(x, y, scale, speed)  # Llama al constructor de la clase padre (player_game)
        # Carga las imágenes de los enemigos desde las hojas de sprites y las redimensiona
        self.enemy_run = Auxiliar_2.getSurfaceFromSpriteSheet(run_enemy)
        self.enemy_run = [pg.transform.scale(img, (int(img.get_width() * SCALE_ENEMY), int(img.get_height() * SCALE_ENEMY))) for img in self.enemy_run]
        self.image_enemy = Auxiliar_2.getSurfaceFromSpriteSheet(enemy)
        self.image_enemy = [pg.transform.scale(img, (int(img.get_width() * SCALE_ENEMY), int(img.get_height() * SCALE_ENEMY))) for img in self.image_enemy]
        self.dead = Auxiliar_2.getSurfaceFromSpriteSheet(death_enemy)
        self.dead = [pg.transform.scale(img , (int(img.get_width() * SCALE_ENEMY), int(img.get_height() * SCALE_ENEMY))) for img in self.dead]
        self.animation_speed = animation_speed
        self.y = y
        self.update_time = None
        self.speed = speed
        self.frame = 0
        self.state_death = False
        self.death_count = 0
        self.alivee = True
        self.death_animation_played = False
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
        self.vision = pg.Rect(0, 0, 150, 20)
        self.ammo = 200
        self.bullet_group_enemy = pg.sprite.Group()

    def moving(self, moving_left, moving_right):
        # Método para establecer la dirección de movimiento del enemigo
        if self.alivee:
            if moving_left:
                self.dx = -self.speed
                self.flip = True
                self.animation = self.enemy_run
            elif moving_right:
                self.dx = self.speed
                self.flip = False
                self.animation = self.enemy_run
            else:
                self.moving_left = False
                self.moving_right = False
                self.animation = self.image_enemy

            if self.health <= 0 and not self.death_state:
                self.health = 0
                self.speed = 0
                self.alivee = False

    def ai(self, player, screen, enemy, scrool):
        # Método para la inteligencia artificial del enemigo
        if player.alivee:
            if not self.idling and random.randint(1, 60) == 1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 20

            if self.vision.colliderect(enemy.rect):
                self.update_action(0)
                self.shoot_bullet(self.bullet_group_enemy)
                self.moving_left = False
                self.moving_right = False
                self.animation = self.image_enemy
                self.dx = 0
            else:
                if not self.idling:
                    if self.direction == 1:
                        self.moving_left = False
                        self.moving_right = True
                    elif self.direction < 1:
                        self.moving_left = True
                        self.moving_right = False

                    self.move_counter += 1
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > 13:
                        self.direction *= -1
                        self.move_counter *= -1
                elif self.idling:
                    self.moving_left = False
                    self.moving_right = False
                    self.animation = self.image_enemy
                    self.dx = 0
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
        self.rect.x += scrool

    def update(self, player,world):
        """Método para actualizar la posición y la animación del enemigo"""
        if self.alivee:
            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= 1
            self.moving(self.moving_left, self.moving_right)

            self.vel_y += GRAVITY
            self.dy += self.vel_y

            if self.rect.bottom + self.dy > self.y:
                self.dy = self.y - self.rect.bottom
                self.in_air = False
                self.jumping = False
                self.rect.y = self.y

            self.rect.x += self.dx
            self.rect.y += self.dy
            self.bullet_group_enemy.update()
            for bullet in self.bullet_group_enemy:

                if pg.sprite.spritecollide(player, self.bullet_group_enemy, False):
                    if player.alivee:
                        player.health -= 10
                        bullet.kill()
                for tile in world.obstacle_list:
                    if tile[1].colliderect(bullet.rect):
                        bullet.kill()
        # Eliminar las balas que está

        if not self.alivee:
            self.bullet_group_enemy.empty()
        if not self.alivee:
            self.animation = self.dead
        if not self.alivee:
            if not self.animation_death:
                self.animation = self.dead
                self.animation_death = True
                self.frame = 0
                self.update_action(8)
            elif self.frame < len(self.animation) - 1:
                self.frame += 1
            elif self.animation_death:
                self.frame = 7

        if self.alivee:
            current_time = pg.time.get_ticks()
            if self.update_time is None or current_time - self.update_time > self.animation_speed:
                self.update_time = current_time
                if self.frame < len(self.animation) - 1:
                    self.frame += 1
                else:
                    self.frame = 0

    def draw(self, screen):
        """Método para dibujar al enemigo en la pantalla"""
        if self.frame < len(self.animation) - 1:
            self.image = self.animation[self.frame]
        screen.blit(pg.transform.flip(self.image, self.flip, False), self.rect)
