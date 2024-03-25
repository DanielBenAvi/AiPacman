# Example file showing a basic pygame "game loop"
import pygame
from Settings.game_settings import *
from game_manager import GameManager
from draw import *
from Settings.colors import *

# pygame setup
pygame.init()
pygame.display.set_caption("Pacman")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
start_run_time = pygame.time.get_ticks()
# ################# GAME MANAGER ##################
gameManager = GameManager()

# ################# EVENTS ##################
pygame.time.set_timer(MOVE_PACMAN, 250)
pygame.time.set_timer(MOVE_GHOST, 500)
pygame.time.set_timer(REGENERATE_COINS, 1000)
pygame.time.set_timer(DESTROY_COINS, 2000)


def change_run_mode(status: bool):
    global start_run_time
    current_time = pygame.time.get_ticks()
    if current_time - start_run_time >= 500:
        gameManager.pacman.run_mode = status
        start_run_time = pygame.time.get_ticks()


# game loop
while running:
    # check if pacman is no longer threatened
    if gameManager.calculate_num_of_threatening_ghosts() == 0:
        change_run_mode(False)

    # check if pacman is threatened
    if gameManager.calculate_num_of_threatening_ghosts() == 1:
        change_run_mode(True)

    # check if game is over
    if gameManager.calculate_num_of_threatening_ghosts() > 1:
        running = False
        print("Too many ghosts! Game over!")

    gameManager.check_collision()
    if gameManager.pacman.eaten_by_ghost:
        running = False
        print("Pacman was eaten by a ghost")

    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():  # get all events in the last 1/60th of a second
        if event.type == pygame.QUIT:  # if the user clicked X
            running = False
        if event.type == REGENERATE_COINS:  # regenerate coins
            gameManager.add_coin()
        if event.type == DESTROY_COINS:  # destroy coins
            gameManager.remove_coin()
        if event.type == MOVE_PACMAN:  # move pacman
            if gameManager.pacman.run_mode:  # if pacman is threatened by a ghost
                gameManager.run_away_pacman()
            else:
                gameManager.move_pacman()
        if event.type == MOVE_GHOST:  # move all ghosts
            for i in range(len(gameManager.ghosts)):
                gameManager.move_ghost(i, screen)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # ################# DRAW ##################
    draw_maze(screen, gameManager.maze)
    draw_coins(screen, gameManager.list_of_coins)
    gameManager.pacman.draw(screen)
    for ghost in gameManager.ghosts:
        ghost.draw(screen)

    # ################# TEXT ##################
    font = pygame.font.Font(None, 36)

    # Coin counter
    text = font.render(f"Coins: {gameManager.coin_counter}", True, WHITE)
    screen.blit(text, (10, 10))

    # Pacman mode
    text = font.render(f"Threatening: {gameManager.calculate_num_of_threatening_ghosts()}", True, WHITE)
    screen.blit(text, (10, 40))

    # ################# END DRAW ##################
    pygame.display.flip()  # updates the screen
    clock.tick(60)  # limits FPS to 60

pygame.quit()
