from dataclasses import dataclass
import pygame
from Settings.game_settings import *
from Settings.colors import *


@dataclass
class Coin:
    row: int
    col: int
    active: bool

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.active = True

    def draw(self, screen):
        pygame.draw.circle(screen, GOLD,
                           (self.col * TILE_SIZE + TILE_SIZE // 2, self.row * TILE_SIZE + TILE_SIZE // 2),
                           TILE_SIZE // 4)
        pygame.draw.circle(screen, BLACK,
                           (self.col * TILE_SIZE + TILE_SIZE // 2, self.row * TILE_SIZE + TILE_SIZE // 2),
                           TILE_SIZE // 4, 1)

    def collect(self):
        self.active = False
        