from dataclasses import dataclass
import pygame
from Settings.game_settings import *
from Settings.colors import *
from Objects.Node import Node


@dataclass
class Ghost:
    row: int
    col: int
    color: tuple

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.attack_mode = False
        self.attack_mode_start_time = 0

    def draw(self, screen):
        # draw ghost triangle
        pygame.draw.polygon(screen, self.color, [(self.col * TILE_SIZE + TILE_SIZE // 2, self.row * TILE_SIZE),
                                                 (self.col * TILE_SIZE, self.row * TILE_SIZE + TILE_SIZE),
                                                 (self.col * TILE_SIZE + TILE_SIZE, self.row * TILE_SIZE + TILE_SIZE)])

        # circle with radius as attack distance around ghost
        pygame.draw.circle(screen, LIGHT_PINK, (self.col * TILE_SIZE + TILE_SIZE // 2, self.row * TILE_SIZE + TILE_SIZE // 2), ATTACK_DISTANCE * TILE_SIZE, 1)
