import pygame as pg
from pygame.sprite  import *
from constantes_crisis  import * 
import csv
from player import player_game
from bar_health import health_bar
from item_box import itemBox
from enemy import enemys
from decoration import decoration
from lava import lava
from exit import exits

class world():
    def __init__(self) -> None:
        self.obstacle_list = []
        
    def pocess_data(self,data,levels):
        """"Procesa los datos del nivel para crear el mundo y los objetos correspondientes"""
        for x in range(title_types):
            img = pg.image.load(f"img\\tile\\{x}.png")
            img = pg.transform.scale(img , (tile_size , tile_size))
            img_list.append(img)

        for row in range(rows):
            r = [-1] * cols
            world_data.append(r)  

        with open(f"level{levels}_data.csv",newline="") as csvfile:
            reader = csv.reader(csvfile,delimiter=",")
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile) 
                                    
        self.level_length = len(data[0])
        player_1 = None
        bar_health = None
        
        for y,row in enumerate(data):
            for x,tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * tile_size 
                    img_rect.y = y * tile_size
                    img_rect.width -= 14
                    tile_data = (img, img_rect)

                    if tile >= 0 and tile <= 8:
        
                        self.obstacle_list.append(tile_data)
                    elif tile > 8 and tile < 11:
                        lav = lava(img , x * tile_size ,y * tile_size)
                        LAVA_GROUP.add(lav)
                        
                    elif tile >= 11 and tile <= 14:
                        decorations = decoration(img , x * tile_size ,y * tile_size)
                        DECORATIOS_GROUP.add(decorations)
                        
                    elif tile == 15: #create player
                        player_1 = player_game( x * tile_size , y  ,7.65,15)
                        player_1.alivee = True
                        bar_health = health_bar(10,5,player_1.health,player_1.health)
                    elif tile == 16:#create enemis
                        enemy = enemys(x * tile_size, y * tile_size + 17, 8, 6, 90)
                        ENEMY_GROUP.add(enemy)
                    elif tile == 17: #create ammo box
                        item_box_ammo = itemBox("ammo" , x * tile_size ,y * tile_size)
                        ITEMS_GROUP.add(item_box_ammo)
                    elif tile == 18:
                        item_box_granade = itemBox("granade",x * tile_size, y * tile_size)
                        ITEMS_GROUP.add(item_box_granade) 
                    elif tile == 20: #create exit
                        ex = exits(img , x * tile_size ,y * tile_size)
                        EXIT_GROUP.add(ex)
                        
                        
        return player_1 ,bar_health 


    def draw(self , screen , scroll ):
        for tile in self.obstacle_list:
            tile[1][0] += scroll
            screen.blit(tile[0], tile[1])
            # pg.draw.rect(screen, (255, 0, 0), tile[1], 2)

