import pygame as pg
from constantes_crisis import *
from auxiliar import *
from levels import world
import csv

# Inicialización de Pygame y configuración de la pantalla
pg.display.init()
pg.font.init()
pygame.mixer.init()
clock = pg.time.Clock()
pantalla = pg.display.set_mode((ANCHO_PANTALLA,ALTO_PANTALLA))
pg.display.set_caption("CRISIS")

# Variables y configuraciones iniciales
slide_time = 0
run = True
world_ = world()
FONT = pg.font.SysFont('futura',23)
background_game = pygame.image.load(r"img\fondos\level1.jpeg").convert()

while run:
    keys = pg.key.get_pressed()
    pantalla.fill((144,144,144))

    for event in pg.event.get():
        keys = pg.key.get_pressed()
        if event.type == pg.QUIT:
            run = False
        
    if not start_game and not start_levels:
        draw_menu(menu_fond,pantalla,ANCHO_PANTALLA,ALTO_PANTALLA)
        if button_start.draw(pantalla):
            level = 1
            start_game = True
            player_1,bar_health , start_game , world_ =loading_level(reset_level,level,csv,world,world_)

        if button_exit.draw(pantalla):
            run = False
        if button_level.draw(pantalla):
            start_levels = True
            print("apretaste")
    if not start_game and start_levels:  
        draw_menu(levels_found,pantalla,ANCHO_PANTALLA,ALTO_PANTALLA) 
        
        if button_level_1.draw(pantalla):
            level = 1
            player_1,bar_health , start_game , world_ =loading_level(reset_level,level,csv,world,world_)
            start_levels = False
            print("nivel 1")

        if button_level_2.draw(pantalla):
            level = 2
            player_1,bar_health , start_game , world_ =loading_level(reset_level,level,csv,world,world_)
            start_levels = False
            print("nivel 2")

        if button_level_3.draw(pantalla):
            level = 3
            player_1,bar_health , start_game , world_ =loading_level(reset_level,level,csv,world,world_)
            print("nivel 3")
            start_levels = False

        
        pg.display.update()
    elif start_game:           
        _scroll  , level_comple = player_1.update(world_,bg_scroll)
        
        print(level_comple)
        bg_scroll -= _scroll
        draw_background(background_game,pantalla,bg_scroll)
        
        # Dibujar al jugador y a las balas
        player_1.draw(pantalla)
        player_1.bullet_group.draw(pantalla)
        if not player_1.flag_pause:
            flag_paused = player_1.events(keys)
            
        # Control de tiempo de disparo y animación
        if player_1.shoot_movent and player_1.shoot_state:
            start_time = pg.time.get_ticks()
        new_time = pg.time.get_ticks() - start_time
        if player_1.shoot_movent and new_time > 150:
            player_1.shoot_movent = False
        if player_1.melee_state and new_time > 0:
            player_1.melee_state = False
            
        # Actualizar y dibujar a los enemigos
        for enemy in ENEMY_GROUP:
            if player_1.alivee and not player_1.flag_pause:
                enemy.ai(enemy,pantalla,player_1,_scroll)
                enemy.update(player_1,world_)
            enemy.draw(pantalla)
            enemy.bullet_group_enemy.draw(pantalla)
            
          # Actualizar y dibujar los objetos del juego
        ITEMS_GROUP.update(player_1,_scroll,sound_box)
        ITEMS_GROUP.draw(pantalla)
        EXPLOSION_GROUP.update()
        EXPLOSION_GROUP.draw(pantalla)
        GRANADE_GROUP.update(player_1,world_ , pantalla,_scroll)
        GRANADE_GROUP.draw(pantalla)
        LAVA_GROUP.update(_scroll)
        LAVA_GROUP.draw(pantalla)
        DECORATIOS_GROUP.update(_scroll)
        DECORATIOS_GROUP.draw(pantalla)
        EXIT_GROUP.update(_scroll)
        EXIT_GROUP.draw(pantalla)
        
        # Mostrar la cantidad de municiones y granadas del jugador
        render_text("AMMO:",FONT,(255,255,255),10,31,pantalla)
        for x in range(player_1.ammo):
            pantalla.blit(BULLET_IMG, (80+ (x * 15), 34))
        render_text("GRANADES:",FONT,(255,255,255),10,54,pantalla)
        for x in range(player_1.ammo_granade):
            pantalla.blit(granade, (130+ (x * 18), 54))
            
        # Dibujar el mundo del juego y la barra de salud del jugador
        world_.draw(pantalla, _scroll)
        bar_health.draw(player_1.health,pantalla)
        #juego en pausa
        if player_1.flag_pause:
            draw_menu(menu_paused,pantalla,ANCHO_PANTALLA  , ALTO_PANTALLA )
            if btn_paus_exit.draw(pantalla):
                run = False
            if btn_paus_back.draw(pantalla):
                player_1.flag_pause = False
            if btn_paus_menu.draw(pantalla):
                player_1.flag_pause =  False
                start_game = False       
            pg.display.update()
            
        # Nivel completado
        if level_comple:
            if  not flag_sound_level_up:
                background_music.stop()
                sound_level_up.play()
                flag_sound_level_up = True
                flag_music_playing = False

            level += 1
            bg_scroll = 0
            player_1,bar_health , start_game , world_ =loading_level(reset_level,level,csv,world,world_)
            
          # Jugador muerto
        if player_1.alivee and not player_1.flag_pause:
            if player_1.alivee and not flag_music_playing:
                background_music.play(-1)
                flag_music_playing = True
                flag_music_game_over = False
                flag_sound_level_up = False
        
            if player_1.granade:
                player_1.shoot_granade()
            if player_1.sped_lef_shoot:
                player_1.shoot_bullet(player_1.bullet_group)
                player_1.sped_lef_shoot = False
                player_1.update_action(4)
            if player_1.shoot_state:
                player_1.shoot_bullet(player_1.bullet_group)
                player_1.shoot_state = False
                player_1.update_action(3)
            if player_1.in_air:
                player_1.update_action(2)
            elif player_1.moving_left or player_1.moving_right:
                player_1.update_action(1)
            else:
                player_1.update_action(0)
        elif not player_1.alivee:
            background_music.stop()
            if not flag_music_game_over:
                sound_game_over.play()
                flag_music_playing = False
                flag_music_game_over = True
            screen_scroll = 0  
            bg_scroll = 0
            if button_restart.draw(pantalla):
                player_1,bar_health , start_game , world_ =loading_level(reset_level,level,csv,world,world_)
            
    clock.tick(FPS)
    pg.display.update()
