import pygame 
from button import Button

def loading_level(reset,level,csv,world,world_):
    """"Función para cargar un nivel"""
    if level > 3:
        level = 1
    world_dat = reset(world_)
    with open(f"level{level}_data.csv",newline="") as csvfile:
            reader = csv.reader(csvfile,delimiter=",")
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_dat[x][y] = int(tile)
    world_ = world()    
    player_1 , bar_health = world_.pocess_data(world_dat,level)
    start_game = True
    return player_1 , bar_health , start_game ,world_

def draw_menu(path,screen,width,heidth):
    """"Función para dibujar un menú"""
    menu = pygame.image.load(path)
    menu = pygame.transform.scale(menu,(width,heidth))
    screen.blit(menu, (0, 0))

def draw_background(img,screen,scroll):
    """ Función para dibujar el fondo del juego"""
    img = pygame.transform.scale(img , (800,700))
    width = img.get_width()
    for x in range(8):
        screen.blit(img,((x * width) - scroll,0))

def render_text(text,font,text_col , x, y,screen) -> None:
    """ Función para renderizar texto en la pantalla"""
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))
    
# def img_text(player,img,cordenadas,screen,ammos):
#     for x in range(player.ammos):
#         screen.blit(img, cordenadas)
        
def draw_background(img,screen,scroll):
    """ Función para renderizar texto en la pantalla"""
    img = pygame.transform.scale(img , (800,700))
    width = img.get_width()
    for x in range(8):
        screen.blit(img,((x * width) - scroll,0))
   
class Auxiliar_2:
    """ Función para cargar imágenes de una hoja de sprites  """
    @staticmethod
    def getSurfaceFromSpriteSheet(paths):
        lista = []
        for path in paths:
            surface_imagen = pygame.image.load(path)     
            lista.append(surface_imagen)
        return lista
    
# Definición de rutas a imágenes
shoot = [r"img\G.U.N SEPARADO POR NEO GYL\robot\Shoot ({0}).png".format(i)for i in range(1,5)]
melee = [r"img\G.U.N SEPARADO POR NEO GYL\robot\Melee ({0}).png".format(i)for i in range(1,9)]
dead_player = [r"img\G.U.N SEPARADO POR NEO GYL\robot\Dead ({0}).png".format(i)for i in range(1,11)]
idle = [r"img\G.U.N SEPARADO POR NEO GYL\robot\Idle ({0}).png".format(i)for i in range(1,11)]
jump_atack_melee = [r"img\G.U.N SEPARADO POR NEO GYL\robot\JumpMelee ({0}).png".format(i)for i in range(1,9)]
run_shoot = [r"img\G.U.N SEPARADO POR NEO GYL\robot\RunShoot ({0}).png".format(i)for i in range(1,10)]
jumpp = [r"img\G.U.N SEPARADO POR NEO GYL\robot\Jump ({0}).png".format(i) for i in range(6,7)]
slide = [r"img\G.U.N SEPARADO POR NEO GYL\robot\Slide ({0}).png".format(i) for i in range(1,11)]
enemy = [f"img\\G.U.N SEPARADO POR NEO GYL\\enemy\\Idle\\{i}.png" for i in range(0,5)]
run_enemy = [f"img\\G.U.N SEPARADO POR NEO GYL\\enemy\\Run\\{i}.png" for i in range(0,6)]
death_enemy = [f"img\\G.U.N SEPARADO POR NEO GYL\\enemy\\Death\\{i}.png" for i in range(0,8)]
granade = pygame.image.load(r"img\G.U.N SEPARADO POR NEO GYL\icons\grenade.png")
# granade_box = pygame.image.load(r"img\G.U.N SEPARADO POR NEO GYL\icons\grenade_box.png")
explosion = [r"img\G.U.N SEPARADO POR NEO GYL\explosion\exp{0}.png".format(i) for i in range(1,6)]

heal_box_img = pygame.image.load(r"img\G.U.N SEPARADO POR NEO GYL\icons\health_box.png")
ammo_box_img = pygame.image.load(r"img\G.U.N SEPARADO POR NEO GYL\icons\ammo_box.png")
grnade_box_img = pygame.image.load(r"img\G.U.N SEPARADO POR NEO GYL\icons\grenade_box.png")

item_boxes = {
    "health" :  heal_box_img,
    "ammo" : ammo_box_img,
    "granade" : grnade_box_img
}
#fondos , menus
menu_paused = r"img\menu\fondo_paused.jpg"
menu_fond= "img\\menu\\fondo_menu.jpg"
levels = "img\\menu\\levels.jpg"
levels_found = "img\\menu\\fondo_levels_png.png"
#botones menus
img_button_restart = pygame.image.load(r"img\menu\restart_btn.png")
img_button_Start = pygame.image.load("img\\menu\\start_btn.png")
img_button_exit = pygame.image.load(r"img\menu\exit_btn.png")
img_button_level = pygame.image.load(r"img\menu\button_level2.jpg")
button_restart = Button(290,290,img_button_restart,2)

button_exit = Button(200,250,img_button_exit,1)
button_start = Button(430,250,img_button_Start,1)
button_level = Button(350,365,img_button_level,1)

img_button_lv_1 = pygame.image.load(r"img\menu\button_lelvel_1.png")
img_button_lv_2 = pygame.image.load(r"img\menu\button_lelvel_2.png")
img_button_lv_3 = pygame.image.load(r"img\menu\button_lelvel_3.png")

button_level_1 = Button(350,160,img_button_lv_1,2)
button_level_2 = Button(345,220,img_button_lv_2,2)
button_level_3 = Button(350,280,img_button_lv_3,2)

img_btn_paus_back = pygame.image.load(r"img\menu\btn_back_paused.jpg")
img_btn_paus_menu = pygame.image.load(r"img\menu\btn_menu_paused.jpg")
img_btn_paus_exit = pygame.image.load(r"img\menu\btn_quit_paused.jpg")

btn_paus_exit = Button(200,260,img_btn_paus_exit,1)
btn_paus_menu = Button(430,250,img_btn_paus_menu,1)
btn_paus_back = Button(350,365,img_btn_paus_back,1)
