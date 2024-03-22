import pygame
from Settings.game_settings import *
from Settings.colors import *


def draw_maze(screen, maze):
    for row in range(28):
        for col in range(28):
            if maze[row][col] == 0:
                draw_tile(screen, row, col, BLACK, BLACK)
            elif maze[row][col] == 1:
                draw_tile(screen, row, col, BLUE, BLACK)
            elif maze[row][col] == 2:
                draw_tile(screen, row, col, BLACK, BLACK)
            else:
                print("Invalid maze value")


def draw_tile(screen, row, col, fill, outline):
    pygame.draw.rect(screen, fill, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(screen, outline, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)


def draw_coins(screen, coins):
    for coin in coins:
        if coin.active:
            coin.draw(screen)