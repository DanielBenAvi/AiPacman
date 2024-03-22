from dataclasses import dataclass
from Settings.game_settings import *
from Settings.colors import *


@dataclass
class Pacman:
    row: int
    col: int
    num_of_threatening_ghosts: int
    eaten_by_ghost: bool
    run_mode: bool

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.num_of_threatening_ghosts = 0
        self.eaten_by_ghost = False
        self.run_mode = False

    def draw(self, screen):
        color = ORANGE if self.run_mode else YELLOW
        pygame.draw.circle(screen, color,
                           (self.col * TILE_SIZE + TILE_SIZE // 2, self.row * TILE_SIZE + TILE_SIZE // 2),
                           TILE_SIZE // 2)
        pygame.draw.circle(screen, WHITE,
                           (self.col * TILE_SIZE + TILE_SIZE // 2, self.row * TILE_SIZE + TILE_SIZE // 2),
                           TILE_SIZE // 2, 1)



