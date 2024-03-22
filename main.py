# Example file showing a basic pygame "game loop"
import pygame
from Settings.game_settings import *
from game_manager import GameManager
from draw import *
from Settings.colors import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

# timer for action events
pygame.time.set_timer(MOVE_PACMAN, 250)
pygame.time.set_timer(MOVE_GHOST, 250)
pygame.time.set_timer(REGENERATE_COINS, 1000)
pygame.time.set_timer(DESTROY_COINS, 1000)

pygame.display.set_caption("Pacman")

gameManager = GameManager()

start_run_time = pygame.time.get_ticks()

# game loop
while running:
    # check if pacman is no longer threatened
    if gameManager.calculate_num_of_threatening_ghosts() == 0:
        current_time = pygame.time.get_ticks()
        if current_time - start_run_time >= 2000:
            gameManager.pacman.run_mode = False
            start_run_time = pygame.time.get_ticks()

    # check if pacman is threatened
    if gameManager.calculate_num_of_threatening_ghosts() == 1:
        current_time = pygame.time.get_ticks()
        if current_time - start_run_time >= 2000:
            gameManager.pacman.run_mode = True
            start_run_time = pygame.time.get_ticks()


    # check if game is over
    if gameManager.calculate_num_of_threatening_ghosts() > 1:
        running = False

    gameManager.check_collision()
    if gameManager.pacman.eaten_by_ghost:
        running = False
        print("Pacman was eaten by a ghost")

    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == REGENERATE_COINS:
            gameManager.add_coin()
        elif event.type == DESTROY_COINS:
            gameManager.remove_coin()
        elif event.type == MOVE_PACMAN:
            if gameManager.pacman.run_mode:
                gameManager.run_away_pacman()
            else:
                gameManager.move_pacman()
        elif event.type == MOVE_GHOST:
            for i in range(len(gameManager.ghosts)):
                if gameManager.calculate_distance_to_pacman(i) <= ATTACK_DISTANCE:
                    gameManager.move_ghost(i, screen)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE
    draw_maze(screen, gameManager.maze)
    draw_coins(screen, gameManager.list_of_coins)
    gameManager.pacman.draw(screen)
    for ghost in gameManager.ghosts:
        ghost.draw(screen)

    # WRITE TEXT HERE
    font = pygame.font.Font(None, 36)

    # Coin counter
    text = font.render(f"Coins: {gameManager.coin_counter}", True, WHITE)
    screen.blit(text, (10, 10))

    # Pacman mode
    text = font.render(f"Threatening: {gameManager.calculate_num_of_threatening_ghosts()}", True, WHITE)
    screen.blit(text, (10, 40))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
