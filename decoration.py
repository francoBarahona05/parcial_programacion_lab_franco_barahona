import pygame as pg
from lava import lava

class decoration(lava):
    def __init__(self, img, x, y) -> None:
        super().__init__(img, x, y)
        
    def update(self, scroll):
        super().update(scroll)
