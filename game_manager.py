from dataclasses import dataclass
from math import sqrt

from Objects.Node import Node
from Objects.coin import Coin
from random import random

from Objects.ghost import Ghost
from Objects.pacman import Pacman
from Settings.colors import *
from Settings.game_settings import *
from Settings.priorityQueue import PriorityQueue


def generate_maze() -> list[list[int]]:
    maze = [[0 for _ in range(NUM_OF_TILES)] for _ in range(NUM_OF_TILES)]
    for row in range(NUM_OF_TILES):
        for col in range(NUM_OF_TILES):
            maze[row][col] = MAZE[row][col]
    return maze


def init_queue(game_object: Pacman | Ghost):
    queue: list[Node] = [Node(game_object.row, game_object.col, None)]
    return queue


def restore_path(direction, node, row, col, game_object: Pacman | Ghost):
    # If the node is a coin, return the path
    tmp_row, tmp_col = row + direction[0], col + direction[1]
    while node.parent:
        node = node.parent
        # if node is the pacman, break
        if node.row == game_object.row and node.col == game_object.col:
            break
        tmp_row, tmp_col = node.row, node.col
    return tmp_row, tmp_col


@dataclass
class GameManager:
    maze: list[list[int]]
    list_of_coins: list[Coin]
    pacman: Pacman
    ghosts: list[Ghost]
    coin_counter: int = 0

    def __init__(self):
        # generate objects array based on maze
        self.maze = generate_maze()
        # generate coins
        self.list_of_coins = self.generate_coins()
        # generate pacman
        self.pacman = Pacman(1, 1)
        # generate ghosts
        ghost1 = Ghost(1, 26, DARK_BLUE)
        ghost2 = Ghost(26, 26, DARK_GREEN)
        ghost3 = Ghost(26, 1, DARK_PURPLE)
        self.ghosts = []
        self.ghosts.append(ghost1)
        self.ghosts.append(ghost2)
        self.ghosts.append(ghost3)

    def generate_coins(self) -> list[Coin]:
        list_of_coins = []
        for row in range(NUM_OF_TILES):
            for col in range(NUM_OF_TILES):
                if self.maze[row][col] == 0:
                    if random() < 0.1:
                        list_of_coins.append(Coin(row, col))
                        self.maze[row][col] = 2  # 1 means there is a coin
        return list_of_coins

    def add_coin(self):
        row = int(random() * NUM_OF_TILES)
        col = int(random() * NUM_OF_TILES)
        if self.maze[row][col] == 0:
            self.list_of_coins.append(Coin(row, col))
            self.maze[row][col] = 2

    def remove_coin(self):
        """
        Remove a coin from the maze
        """
        if len(self.list_of_coins) > 0:
            coin = self.list_of_coins[0]
            self.list_of_coins.remove(coin)
            self.maze[coin.row][coin.col] = 0

    def move_pacman(self):
        ...
        # Create a queue for BFS
        queue = init_queue(self.pacman)
        # Mark the source node as visited and enqueue it
        visited = [[False for _ in range(NUM_OF_TILES)] for _ in range(NUM_OF_TILES)]

        # Mark the source node as visited and enqueue it
        visited[self.pacman.row][self.pacman.col] = True

        # remove the coin from the list
        self.coin_collision()

        while queue:
            # Dequeue a vertex from queue
            node = queue.pop(0)
            row, col = node.row, node.col

            # add to visited
            visited[row][col] = True

            # Otherwise enqueue its adjacent nodes
            for direction in DIRECTIONS:
                # check not valid
                if not self.is_valid_move(row + direction[0], col + direction[1]):
                    continue

                # check if visited
                if visited[row + direction[0]][col + direction[1]]:
                    continue

                # enqueue the next node
                queue.append(Node(row + direction[0], col + direction[1], node))

                if self.maze[row + direction[0]][col + direction[1]] != 2:
                    continue

                # If the node is a coin, return the path
                tmp_row, tmp_col = restore_path(direction, node, row, col, self.pacman)

                # move the pacman to the next step
                self.move_direction(tmp_row, tmp_col, self.pacman)

                return

    def coin_collision(self):
        for coin in self.list_of_coins:
            if coin.row == self.pacman.row and coin.col == self.pacman.col:
                coin.collect()
                self.list_of_coins.remove(coin)
                self.maze[self.pacman.row][self.pacman.col] = 0
                self.coin_counter += 1
                break

    def move_direction(self, tmp_row, tmp_col, game_object: Pacman | Ghost, direction: int = 1):
        temp_direction = (0, 0)
        if tmp_row < game_object.row:
            temp_direction = NEW_DIRECTIONS["UP"]
        # if node is down from the pacman
        elif tmp_row > game_object.row:
            temp_direction = NEW_DIRECTIONS["DOWN"]
        # if node is left from the pacman
        elif tmp_col < game_object.col:
            temp_direction = NEW_DIRECTIONS["LEFT"]
        # if node is right from the pacman
        elif tmp_col > game_object.col:
            temp_direction = NEW_DIRECTIONS["RIGHT"]

        temp_direction = (temp_direction[0] * direction, temp_direction[1] * direction)

        if self.is_valid_move(game_object.row + temp_direction[0], game_object.col + temp_direction[1]):
            game_object.row += temp_direction[0]
            game_object.col += temp_direction[1]

    def run_away_pacman(self):
        # Create a queue for BFS
        queue = init_queue(self.pacman)

        # Mark the source node as visited and enqueue it
        visited = {(self.pacman.row, self.pacman.col): True}

        # remove the coin from the list
        self.coin_collision()

        while queue:
            # Dequeue a vertex from queue
            node = queue.pop(0)
            row, col = node.row, node.col

            # add to visited
            visited[(row, col)] = True

            # Otherwise enqueue its adjacent nodes
            for direction in DIRECTIONS:
                # check if not in bounds
                if not self.is_valid_move(row + direction[0], col + direction[1]):
                    continue

                # check if visited
                if visited.get((row + direction[0], col + direction[1])):
                    continue

                # enqueue the next node
                queue.append(Node(row + direction[0], col + direction[1], node))

                # If the node is a ghost, return the path and move pacman to the opposite direction
                for ghost in self.ghosts:
                    if row + direction[0] == ghost.row and col + direction[1] == ghost.col:
                        tmp_row, tmp_col = restore_path(direction, node, row, col, self.pacman)

                        self.move_direction(tmp_row, tmp_col, self.pacman, -1)

                        return

    def move_ghost(self, current_ghost_index: int, screen: pygame.Surface):
        if len(self.ghosts) == 0:
            return  # no ghosts

        open_list = PriorityQueue()
        closed_list = {}

        # add the starting node to the open list
        start_node = Node(self.ghosts[current_ghost_index].row, self.ghosts[current_ghost_index].col, None)
        start_node.calculate_h(self.pacman.row, self.pacman.col)
        start_node.calculate_f()
        open_list.insert(start_node)

        # while the open list is not empty
        while not open_list.isEmpty():
            # get the current node
            current_node = open_list.delete()
            row, col = current_node.row, current_node.col

            # add to closed list
            closed_list[(row, col)] = True

            for children in DIRECTIONS:
                # check if not in bounds
                if not self.is_valid_move(row + children[0], col + children[1]):
                    continue

                # check if visited
                if closed_list.get((row + children[0], col + children[1])):
                    continue

                # add to open list with the parent and g, h, f values
                node = Node(row + children[0], col + children[1], current_node)
                node.calculate_g(current_node)
                node.calculate_h(self.pacman.row, self.pacman.col)
                node.calculate_f()
                open_list.insert(node)

                # check if pacman
                if row + children[0] == self.pacman.row and col + children[1] == self.pacman.col:
                    # If the node is a coin, return the path
                    tmp_row, tmp_col = restore_path(children, node, row, col, self.ghosts[current_ghost_index])

                    # move the pacman to the next step
                    self.move_direction(tmp_row, tmp_col, self.ghosts[current_ghost_index])

                    return

    def calculate_distance_to_pacman(self, ghost: int):
        return sqrt((self.pacman.row - self.ghosts[ghost].row) ** 2 + (self.pacman.col - self.ghosts[ghost].col) ** 2)

    def calculate_num_of_threatening_ghosts(self):
        self.pacman.num_of_threatening_ghosts = 0
        for i, ghost in enumerate(self.ghosts):
            if self.calculate_distance_to_pacman(i) < ATTACK_DISTANCE:
                self.pacman.num_of_threatening_ghosts += 1
        return self.pacman.num_of_threatening_ghosts

    def check_collision(self):
        for ghost in self.ghosts:
            if self.pacman.row == ghost.row and self.pacman.col == ghost.col:
                self.pacman.eaten_by_ghost = True
                return
        return

    def is_valid_move(self, row, col):
        # check if not in bounds
        if row < 0 or row >= NUM_OF_TILES or col < 0 or col >= NUM_OF_TILES:
            return False

        # check if wall
        if self.maze[row][col] == 1:
            return False

        return True
