from game.Cell import Cell
import curses
import random

class Game:
    def __init__(self, n):
        self.high = n
        self.isGameOver = False
        self.board = self.create_board()
        self.score = 0
        self.nr_bombs = n + int(n/2) + int(n/3)
        self.bomb_locations = []
        self.flags_put = 0

    def create_board(self):
        outer = [None] * self.high
        for i in range(self.high):
            outer[i] = [None] * self.high
            for c in range(self.high):
                outer[i][c] = Cell()
        return outer

    def is_game_over(self):
        for b in self.board:
            for c in b:
                if c.hasExploded:
                    self.isGameOver = True
        return self.isGameOver

    def put_flag(self, x, y):
        if not self.board[y][x].is_flagged() and not self.board[y][x].has_opened():
            cells = self.board[y]
            cells[x].set_flagged(True)
            self.board[y] = cells
            self.flags_put += 1
        elif self.board[y][x].is_flagged():
            self.board[y][x].set_flagged(False)
            self.flags_put -= 1

    def print_board(self, stdscr):
        curr_y, curr_x = curses.getsyx()
        for x in range(self.high):
            for y in range(self.high):
                c = self.get_char(y, x)
                pair = self.get_color_pair(c)
                nb = self.board[y][x].neighbours
                if x is curr_x and y is curr_y:
                    stdscr.addstr(y, x, c, curses.color_pair(16))
                    continue
                if nb > 0 and self.board[y][x].has_opened():
                    if nb == 1:
                        stdscr.addstr(y, x, c, curses.color_pair(7))
                    elif nb == 2:
                        stdscr.addstr(y, x, c, curses.color_pair(8))
                    elif nb == 3:
                        stdscr.addstr(y, x, c, curses.color_pair(9))
                    else:
                        stdscr.addstr(y, x, c, curses.color_pair(10))
                    continue
                stdscr.addstr(y, x, c, curses.color_pair(pair))

    def get_char(self, x, y):
        cells = self.board[x]
        if cells[y].is_flagged():
            return "F"
        elif cells[y].has_opened():
            if cells[y].hasExploded:
                return "*"
            return str(cells[y].neighbours)
        else:
            return "O"

    @staticmethod
    def get_color_pair(c):
        if c == "F":
            return 4
        elif c == "*":
            return 3
        elif c == "O":
            return 1
        else:
            return 5

    def generate_bombs(self):
        for i in range(self.nr_bombs):
            self.place_bomb()
        self.neighbours()

    def place_bomb(self):
        r = random.randint(0, self.high - 1)
        c = random.randint(0, self.high - 1)
        if self.board[r][c].is_a_bomb():
            self.place_bomb()
        else:
            self.board[r][c].set_is_bomb(True)
            self.bomb_locations.append((r, c))

    def reveal(self, x, y):
        if not self.board[y][x].has_opened() and not self.board[y][x].is_flagged():
            self.board[y][x].open(True)
            if not self.board[y][x].has_gotten_points:
                self.score += self.board[y][x].neighbours
                self.board[y][x].has_gotten_points = True
            if self.board[y][x].is_a_bomb():
                self.board[y][x].exploded()
            elif self.board[y][x].neighbours == 0:
                self.open_all_zeros([(x-1, y), (x+1, y), (x, y-1), (x, y+1)])

    def neighbours(self):
        for row in range(0, self.high):
            for col in range(0, self.high):
                if not self.board[row][col].is_a_bomb():
                    self.board[row][col].neighbours = self.calc_neighbours(
                        [(row, col-1), (row-1, col-1), (row+1, col-1), (row+1, col), (row+1, col+1), (row, col+1),
                         (row-1, col+1), (row-1, col)])

    def calc_neighbours(self, coords):
        i = 0
        for row, col in coords:
            if -1 < row < self.high and -1 < col < self.high:
                if self.board[row][col].is_a_bomb():
                    i += 1
        return i

    def open_all_zeros(self, coords):
        for x, y in coords:
            if -1 < x < self.high and -1 < y < self.high:
                if not self.board[y][x].has_opened():
                    self.reveal(x, y)

    def win(self):
        i = 0
        for row in range(self.high):
            for col in range(self.high):
                if self.board[row][col].has_opened():
                    i += 1
        if i + self.flags_put >= (self.high * self.high):
            return True
        return False

    def loose(self):
        lost = False
        for row in range(self.high):
            for col in range(self.high):
                if self.board[row][col].hasExploded:
                    lost = True
        return lost