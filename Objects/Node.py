import dataclasses


@dataclasses.dataclass
class Node:
    row: int
    col: int
    parent: object
    g: int
    h: int
    f: int

    def __init__(self, row, col, parent):
        self.row = row
        self.col = col
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    # getters
    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def get_g(self):
        return self.g

    def calculate_g(self, parent):
        self.g = parent.g + 1

    def calculate_h(self, end_row, end_col):
        self.h = abs(self.row - end_row) + abs(self.col - end_col)

    def calculate_f(self):
        self.f = self.g + self.h
