import pygame as pg
from pygame.sprite import Group
from item_box import itemBox
from pygame import mixer
pg.mixer.init()

# Constantes
ANCHO_PANTALLA = 800
ALTO_PANTALLA = int(ANCHO_PANTALLA * 0.8)
SCROLL_TRESH = 200
screen_scroll = 0
bg_scroll = 0
POS_X = 200
POS_Y = 200
SCALE_PLAYER = 6
SCALE_ENEMY = 1.65
SCALE_RUN_ENEMY = 1.10
FPS = 22
GRAVITY = 1.5
EXIT_GROUP = pg.sprite.Group()
LAVA_GROUP = pg.sprite.Group()
BULLET_GROUP_ENEMYS = pg.sprite.Group()
GRANADE_GROUP = pg.sprite.Group()
EXPLOSION_GROUP = pg.sprite.Group()
ENEMY_GROUP = pg.sprite.Group()
ITEMS_GROUP = pg.sprite.Group()
DECORATIOS_GROUP = pg.sprite.Group()
SCALE_PLAYER = None
SCALE_BULLET = 1.5
SHOOT_COOLDOWN = 10
start_time = 0
AMMO = 5
BULLET_IMG = pg.image.load(r"img\G.U.N SEPARADO POR NEO GYL\icons\bullet.png")
TITLE_SIZE = 40

# Variables de estado del juego
start_game = False
item_box_ = itemBox("health", 100, 550)
ITEMS_GROUP.add(item_box_)
item_box_ammo = itemBox("ammo", 400, 550)
ITEMS_GROUP.add(item_box_ammo)
item_box_granade = itemBox("granade", 500, 550)
ITEMS_GROUP.add(item_box_granade)
game_over_menu = False
start_menu = True
start_levels = False
start_game_over = False
level = 1
flag_paused = False

# Variables del mundo del juego
rows = 16
cols = 150
tile_size = ALTO_PANTALLA // rows
title_types = 21
img_list = []
world_data = []


def reset_level(worlds):
    """
    Restablece el nivel del juego.
    Limpia los grupos de sprites y crea una nueva matriz de datos del mundo.
    """
    ENEMY_GROUP.empty()
    ITEMS_GROUP.empty()
    EXPLOSION_GROUP.empty()
    GRANADE_GROUP.empty()
    LAVA_GROUP.empty()
    DECORATIOS_GROUP.empty()
    EXIT_GROUP.empty()
    data = []
    for row in range(rows):
        r = [-1] * cols
        data.append(r)
    return data

# Comentarios explicativos
# - Importaciones de módulos
# - Definición de constantes
# - Variables de estado del juego
# - Variables del mundo del juego
# - Función reset_level
# flag_music_start = fals
flag_music_playing = False
flag_music_game_over = False
flag_sound_level_up = False

inicio_sound = pg.mixer.Sound(r"sound\01 Stage Start.flac")
inicio_sound.set_volume(0.3)
shott_sound = pg.mixer.Sound(r"sound\shott.wav")
shott_sound.set_volume(0.5)
granade_sound = pg.mixer.Sound(r"sound\explocion.wav")
granade_sound.set_volume(0.5)
jump_sound = pg.mixer.Sound(r"sound\jump.wav")
jump_sound.set_volume(0.3)
background_music = pg.mixer.Sound(r"sound\background music.flac")
background_music.set_volume(0.3)
sound_game_over = pg.mixer.Sound(r"sound\02 Game Over.flac")
sound_game_over.set_volume(0.2)
sound_level_up = pg.mixer.Sound(r"sound\sound_up_level.flac")
sound_level_up.set_volume(0.2)
sound_box = pg.mixer.Sound(r"sound\box.wav")
sound_box.set_volume(0.3)