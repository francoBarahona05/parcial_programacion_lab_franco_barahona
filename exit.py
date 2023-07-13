# from pygame.sprite import _Group
import pygame as pg
from decoration import decoration
# from constantes_crisis import TITLE_SIZE , title_types

class exits(decoration):
    def __init__(self, img, x, y) -> None:
        super().__init__(img, x, y)
