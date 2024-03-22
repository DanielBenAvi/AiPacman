from dataclasses import dataclass
from math import sqrt

from Objects.Node import Node
from Objects.coin import Coin
from random import random

from Objects.ghost import Ghost
from Objects.pacman import Pacman
from Settings.colors import BLUE, RED, GREEN, DARK_BLUE, DARK_GREEN, DARK_PURPLE
from Settings.game_settings import *
from Settings.priorityQueue import PriorityQueue


def generate_maze() -> list[list[int]]:
    maze = [[0 for _ in range(NUM_OF_TILES)] for _ in range(NUM_OF_TILES)]
    for row in range(NUM_OF_TILES):
        for col in range(NUM_OF_TILES):
            maze[row][col] = MAZE[row][col]
    return maze


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
        """
        Add a coin to the maze
        """
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
        """
                Move pacman using bfs algorithm to the nearest coin

        """
        ...
        # Create a queue for BFS
        queue: list[Node] = [Node(self.pacman.row, self.pacman.col, None)]
        # Mark the source node as visited and enqueue it
        visited = [[False for _ in range(NUM_OF_TILES)] for _ in range(NUM_OF_TILES)]

        # Mark the source node as visited and enqueue it
        visited[self.pacman.row][self.pacman.col] = True

        # remove the coin from the list
        for coin in self.list_of_coins:
            if coin.row == self.pacman.row and coin.col == self.pacman.col:
                coin.collect()
                self.list_of_coins.remove(coin)
                self.maze[self.pacman.row][self.pacman.col] = 0
                self.coin_counter += 1
                break
        # self.maze[self.pacman.row][self.pacman.col] = 0

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

                # If the node is a coin, return the path
                if self.maze[row + direction[0]][col + direction[1]] == 2:
                    tmp_row, tmp_col = row + direction[0], col + direction[1]
                    while node.parent:
                        node = node.parent
                        # if node is the pacman, break
                        if node.row == self.pacman.row and node.col == self.pacman.col:
                            break
                        tmp_row, tmp_col = node.row, node.col

                    # move the pacman only one step and not diagonally
                    if tmp_row == self.pacman.row:
                        tmp_row = 0
                    else:
                        tmp_row = 1 if tmp_row > self.pacman.row else -1

                    if tmp_col == self.pacman.col:
                        tmp_col = 0
                    else:
                        tmp_col = 1 if tmp_col > self.pacman.col else -1
                    self.pacman.row += tmp_row
                    self.pacman.col += tmp_col

                    return

    def run_away_pacman(self):
        """
                Move pacman using bfs algorithm
                run from the ghosts
        """
        # Create a queue for BFS
        queue: list[Node] = [Node(self.pacman.row, self.pacman.col, None)]
        # Mark the source node as visited and enqueue it
        visited = [[False for _ in range(NUM_OF_TILES)] for _ in range(NUM_OF_TILES)]

        # Mark the source node as visited and enqueue it
        visited[self.pacman.row][self.pacman.col] = True

        while queue:
            # Dequeue a vertex from queue
            node = queue.pop(0)
            row, col = node.row, node.col

            # add to visited
            visited[row][col] = True

            # Otherwise enqueue its adjacent nodes
            for direction in DIRECTIONS:
                # check if not in bounds
                if not self.is_valid_move(row + direction[0], col + direction[1]):
                    continue

                # check if visited
                if visited[row + direction[0]][col + direction[1]]:
                    continue

                # enqueue the next node
                queue.append(Node(row + direction[0], col + direction[1], node))

                # If the node is a ghost, return the path and move pacman to the opposite direction
                for ghost in self.ghosts:
                    if row + direction[0] == ghost.row and col + direction[1] == ghost.col:
                        # find the path to the ghost
                        tmp_row, tmp_col = row + direction[0], col + direction[1]
                        while node.parent:
                            node = node.parent
                            # if node is the pacman, break
                            if node.row == self.pacman.row and node.col == self.pacman.col:
                                break
                            tmp_row, tmp_col = node.row, node.col

                        # move the pacman only one step and not diagonally
                        if tmp_row == self.pacman.row:
                            tmp_row = 0
                        else:
                            tmp_row = 1 if tmp_row > self.pacman.row else -1

                        if tmp_col == self.pacman.col:
                            tmp_col = 0
                        else:
                            tmp_col = 1 if tmp_col > self.pacman.col else -1

                        if self.is_valid_move(self.pacman.row - tmp_row, self.pacman.col - tmp_col):
                            self.pacman.row -= tmp_row
                            self.pacman.col -= tmp_col
                        else:
                            for new_dir in DIRECTIONS:
                                if self.is_valid_move(self.pacman.row + new_dir[0], self.pacman.col + new_dir[1]):
                                    self.pacman.row += new_dir[0]
                                    self.pacman.col += new_dir[1]
                                    return

                        return

    def move_ghost(self, ghost: int, screen: pygame.Surface):
        if len(self.ghosts) == 0:
            return  # no ghosts

        open_list = PriorityQueue()
        closed_list = {}

        # add the starting node to the open list
        start_node = Node(self.ghosts[ghost].row, self.ghosts[ghost].col, None)
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

                    tmp_row, tmp_col = row + children[0], col + children[1]

                    while node.parent:
                        node = node.parent
                        # if node is the ghost, break
                        if node.row == self.ghosts[ghost].row and node.col == self.ghosts[ghost].col:
                            break
                        tmp_row, tmp_col = node.row, node.col

                    # move the ghost only one step and not diagonally
                    if tmp_row == self.ghosts[ghost].row:
                        tmp_row = 0
                    else:
                        tmp_row = 1 if tmp_row > self.ghosts[ghost].row else -1

                    if tmp_col == self.ghosts[ghost].col:
                        tmp_col = 0
                    else:
                        tmp_col = 1 if tmp_col > self.ghosts[ghost].col else -1
                    self.ghosts[ghost].row += tmp_row
                    self.ghosts[ghost].col += tmp_col

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
