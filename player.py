from typing import Any
import pygame as pg
from pygame.sprite import *
from constantes_crisis import *
from bullet import bullets
from auxiliar import *
from granade import granades
from explosion import granade_explosion

# Definición de la clase del jugador
class player_game(pg.sprite.Sprite):
    def __init__(self, x, y, scale, speed) -> None:
        super().__init__()

        # Cargar las imágenes de las animaciones del jugador
        self.run_shoot = Auxiliar_2.getSurfaceFromSpriteSheet(run_shoot)
        self.shoot_atack = Auxiliar_2.getSurfaceFromSpriteSheet(shoot)
        self.melee = Auxiliar_2.getSurfaceFromSpriteSheet(melee)
        self.jump_melee = Auxiliar_2.getSurfaceFromSpriteSheet(jump_atack_melee)
        self.jump_action = Auxiliar_2.getSurfaceFromSpriteSheet(jumpp)
        self.dead = Auxiliar_2.getSurfaceFromSpriteSheet(dead_player)
        self.stay = Auxiliar_2.getSurfaceFromSpriteSheet(idle)
        self.slide = Auxiliar_2.getSurfaceFromSpriteSheet(slide)
          
        # Escalar las imágenes al tamaño deseado
        self.slide = [pg.transform.scale(img, (int(img.get_width() / scale), int(img.get_height() / scale))) for img in self.slide]
        self.stay = [pg.transform.scale(img, (int(img.get_width() / scale), int(img.get_height() / scale))) for img in self.stay]
        self.run_shoot = [pg.transform.scale(img, (int(img.get_width() / scale), int(img.get_height() / scale))) for img in self.run_shoot]
        self.shoot_atack = [pg.transform.scale(img, (int(img.get_width() / scale), int(img.get_height() / scale))) for img in self.shoot_atack]
        self.melee = [pg.transform.scale(img, (int(img.get_width() / scale), int(img.get_height() / scale))) for img in self.melee]
        self.jump_melee = [pg.transform.scale(img, (int(img.get_width() / scale), int(img.get_height() / scale))) for img in self.jump_melee]
        self.jump_action = [pg.transform.scale(img, (int(img.get_width() / scale), int(img.get_height() / scale))) for img in self.jump_action]
        self.dead = [pg.transform.scale(img, (int(img.get_width() / scale), int(img.get_height() / scale))) for img in self.dead]
        
        self.frame = 0
        self.animation = self.stay
        self.image = self.animation[self.frame] #imagen que voy a representar
        
        # Inicializar las variables y atributos del jugador
        self.update_time = None
        self.y = y
        self.rect = self.image.get_rect()
        self.width = self.image.get_width() - 20
        self.height = self.image.get_height() 

        self.rect.center = (x ,y)
        self.moving_left = False
        self.moving_right = False
        self.jump = False
        self.alivee = True
        self.vel_y = 0
        self.in_air = True
        self.animation_list = []
        self.action = 0
        self.speed = speed
        self.flip = False
        self.direction = 1
        self.dx = 0
        self.dy = 0
        self.health = 100
        self.max_health = self.health
        self.ammo = AMMO
        self.shoot_state = False
        self.shoot_speed = 1100 / len(self.shoot_atack)
        self.shoot_movent = False
        self.sped_lef_shoot = False
        self.jump_shoot_state = False
        self.melee_state = False
        self.shoot_cooldown = 0
        self.jumping = False
        self.shoot_presed = False
        self.time_death = 0
        self.death_count = 0
        self.animation_death = False
        self.death_state = False
        self.granade = False
        self.bullet = bullets(self.rect.centerx + (0.2 * self.rect.size[0] * self.direction ), self.rect.centery, self.direction, BULLET_IMG)
        self.granade_thrown = False
        self.ammo_granade = 5
        self.granade_presed = False
        self.bullet_group = Group()
        self.death_animation_played = False
        self.new_time = 0
        self.flag_pause = False


    def moving(self, moving_left, moving_right):
        self.dx = 0
        self.dy = 0

        # Actualizar la velocidad y dirección en función del movimiento
        if moving_left:
            self.dx = -self.speed
            self.flip = True  # Invertir la imagen horizontalmente
            self.direction = -1
            self.animation = self.run_shoot

        elif moving_right:
            self.dx = self.speed
            self.flip = False  # Invertir la imagen horizontalmente
            self.direction = 1
            self.animation = self.run_shoot
        else:
            self.animation = self.stay

        # Lógica de salto
        if self.jump and not self.in_air:
            self.vel_y = -17
            self.jump = False
            self.in_air = True

        if self.in_air:
            self.animation = self.jump_action
            self.frame = 0
        if self.shoot_movent:
            self.animation = self.shoot_atack
            self.frame = 0
            
        # Lógica de muerte
        if self.health <= 0  and not self.death_state:
            self.health = 0
            self.speed = 0
            self.alivee = False
                
            
    def shoot_granade(self):
        # Disparar una granada si está disponible y la tecla correspondiente está presionada
        if self.granade and not self.granade_thrown and self.ammo_granade > 0:
            granade = granades(self.rect.centerx + (0.5 * self.rect.size[0] * self.direction), self.rect.top, self.direction)
            GRANADE_GROUP.add(granade)
            self.ammo_granade -= 1
            self.granade_thrown = True
            self.update_action(7)

            # print(self.ammo_granade)
            
    def shoot_bullet(self, bullett):
        # Disparar una bala si hay munición disponible y el tiempo de enfriamiento del disparo ha terminado
        if self.ammo > 0 and self.shoot_cooldown == 0:     
            self.bullet = bullets(self.rect.centerx + (0.2 * self.rect.size[0] * self.direction), self.rect.centery, self.direction, BULLET_IMG)
            bullett.add(self.bullet)
            shott_sound.play()
            self.ammo -= 1
            self.shoot_cooldown = SHOOT_COOLDOWN
            self.update_action(6)
        
            

    def update(self, world, bg ) -> None:
        screen_scroll = 0
        self.moving(self.moving_left, self.moving_right)
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        self.vel_y += GRAVITY
        self.dy += self.vel_y
        
        # Colisiones con los obstáculos del mundo
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + self.dx , self.rect.y , self.width, self.height):
                self.dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + self.dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    self.dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    self.jumping = False
                    self.dy = tile[1].top - self.rect.bottom
    
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.rect.x += screen_scroll


        if self.frame < len(self.animation) - 1:
            self.frame += 1
        else:
            self.frame = 0
        # Actualizar las balas
        self.bullet_group.update()
        if pg.sprite.spritecollide(self, LAVA_GROUP, False):
            self.health = 0
        level_complete = False
        #comprueba colision con la bandera del final del juego
        if pg.sprite.spritecollide(self,EXIT_GROUP,False):
            level_complete = True

                
        if self.rect.bottom > ALTO_PANTALLA:
            self.health = 0
        # Colisiones de balas con enemigos y obstáculos
        for bullet in self.bullet_group:
            enemy_hit = pg.sprite.spritecollideany(bullet, ENEMY_GROUP)
            if enemy_hit and enemy_hit.alivee:
                enemy_hit.health -= 25
                # print(enemy_hit.health)
                bullet.kill()
            for tile in world.obstacle_list:
                if tile[1].colliderect(bullet.rect):
                    bullet.kill()
        # Eliminar las balas que están fuera de la pantalla
        self.bullet_group = pg.sprite.Group([bullet for bullet in self.bullet_group if bullet.rect.right >= 0 and bullet.rect.left <= ANCHO_PANTALLA])
        if not self.alivee:
            self.animation = self.dead
            self.frame = 7
        # Si el jugador está cerca de los bordes de la pantalla, desplazar el fondo
        if (self.rect.right > ANCHO_PANTALLA - SCROLL_TRESH and bg < (world.level_length * tile_size) - ANCHO_PANTALLA) or (self.rect.left < SCROLL_TRESH and bg > abs(self.dx)):
            self.rect.x -= self.dx
            screen_scroll = -self.dx
 
        return screen_scroll , level_complete
            
    def update_action(self, new_action):
        # Actualizar la acción del jugador (cambio de animación)
        if new_action != self.action:
            self.action = new_action
            self.frame = 0 
            self.update_time = pg.time.get_ticks()
            
    def events(self, keys):
        # Manejar los eventos de teclado
        if self.alivee  :
            if keys[pg.K_a] and not keys[pg.K_d]:
                self.moving_left = True
                self.moving_right = False
            elif keys[pg.K_d] and not keys[pg.K_a]:
                self.moving_right = True
                self.moving_left = False

            else:
                self.moving_right = False
                self.moving_left = False  
            if keys[pg.K_w] and not self.jumping:
                self.jump = True
                self.jumping = True
                jump_sound.play()
            if keys[pg.K_j] and not keys[pg.K_d] and not keys[pg.K_a] and not self.shoot_presed:
                self.shoot_state = True
                self.shoot_movent = True
                self.shoot_presed = True

            elif not keys[pg.K_j]:
                self.shoot_presed = False

            if keys[pg.K_d] and keys[pg.K_j] and not self.shoot_presed:
                self.sped_lef_shoot = True
                self.shoot_presed = True
                self.moving_right = True
                self.moving_left = False
            elif keys[pg.K_d] and not keys[pg.K_j]:
                self.shoot_presed = False

            if keys[pg.K_a] and keys[pg.K_j] and not self.shoot_presed:
                self.sped_lef_shoot = True
                self.shoot_presed = True
                self.moving_right = False
                self.moving_left = True
            elif keys[pg.K_a] and not keys[pg.K_j]:
                self.shoot_presed = False
            if keys[pg.K_SPACE] and not self.granade_presed:
                self.granade = True
                self.granade_thrown = False
                self.granade_presed = True
            elif not keys[pg.K_SPACE]:
                self.granade_presed = False
            if keys[pg.K_ESCAPE]:
                self.flag_pause = True
        

    def draw(self, screen):
        # Dibujar el jugador en la pantalla
        self.image = self.animation[self.frame]
        screen.blit(pg.transform.flip(self.image, self.flip, False), self.rect)
