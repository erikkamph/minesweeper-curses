import curses
import os
import random
import re
from curses.textpad import Textbox, rectangle
import time


class Cell:
    def __init__(self):
        self.hasBomb = False
        self.hasExploded = False
        self.flagged = False
        self.is_opened = False
        self.neighbours = 0
        self.flagged_bomb = False
        self.has_gotten_points = False

    def set_flagged(self, b):
        if self.hasBomb:
            self.flagged_bomb = True
        self.flagged = b

    def is_flagged(self):
        return self.flagged

    def get_fb(self):
        return self.flagged_bomb

    def open(self, b):
        self.is_opened = b

    def has_opened(self):
        return self.is_opened

    def is_a_bomb(self):
        return self.hasBomb

    def set_is_bomb(self, b):
        self.hasBomb = True

    def exploded(self):
        self.hasExploded = True


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


def do_something(x, y, c, g):
    new_x = x
    new_y = y
    n = g.high
    if c in ("a", "A", "KEY_LEFT"):
        if x > 0:
            new_x -= 1
    elif c in ("s", "S", "KEY_DOWN"):
        if y < (n - 1):
            new_y += 1
    elif c in ("d", "D", "KEY_RIGHT"):
        if x < (n - 1):
            new_x += 1
    elif c in ("w", "W", "KEY_UP"):
        if y > 0:
            new_y -= 1
    elif c in ("q", "q"):
        g.isGameOver = True
    elif c in ("f", "F"):
        g.put_flag(x, y)
    elif c in ("r", "R"):
        g.reveal(x, y)
    return new_x, new_y


def print_help(stdscr, g):
    text = "Movement: "
    w = "w, up arrow - go up one step"
    a = "a, left arrow - go left one step"
    s = "s, down arrow - go down one step"
    d = "d, right arrow - go right one step"
    f = "f - flag current position"
    r = "r - open current position"
    q = "q - quit the program"
    from_right = g.high + 2
    stdscr.addstr(0, from_right, text, curses.color_pair(2) + curses.A_BOLD)
    stdscr.addstr(1, from_right, w, curses.A_NORMAL)
    stdscr.addstr(2, from_right, a, curses.A_NORMAL)
    stdscr.addstr(3, from_right, s, curses.A_NORMAL)
    stdscr.addstr(4, from_right, d, curses.A_NORMAL)
    stdscr.addstr(5, from_right, f, curses.A_NORMAL)
    stdscr.addstr(6, from_right, r, curses.A_NORMAL)
    stdscr.addstr(7, from_right, q, curses.A_NORMAL)
    stdscr.addstr(8, from_right, "Score: ", curses.A_BOLD + curses.color_pair(2))
    stdscr.addstr(8, from_right + len("Score: ") + 2, str(g.score), curses.A_NORMAL + curses.color_pair(1))
    stdscr.addstr(9, from_right, "Win: " + str(g.win()), curses.A_BOLD + curses.color_pair(2))


def welcome(stdscr):
    string = "Enter a size to use for the board:"
    stdscr.addstr(0, 1, string)
    stdscr.addstr(4, 1, "Help to the right side of board")
    stdscr.addstr(5, 1, "Don't make it smaller than 4 by 4")
    stdscr.addstr(6, 1, "But not bigger than 39 by 39")
    stdscr.addstr(7, 1, "Or get lucky islands revealing small")
    stdscr.addstr(8, 1, "islands of zeros that do not make the game crash")
    stdscr.addstr(9, 1, "Input one value only, not 4x4 or 4*4.")
    stdscr.addstr(10, 1, "Don't make it bigger than number ")
    stdscr.addstr(11, 1, "of rows in terminal! Good Luck!")
    editwin = curses.newwin(1, len(string), 2, 1)
    rectangle(stdscr, 1, 0, 1 + 1 + 1, 1 + len(string))
    stdscr.refresh()
    box = Textbox(editwin)
    box.edit()
    c = box.gather()
    if re.search("[A-Za-z]+", c) or c == "":  # Test if c contains any character
        return 0
    else:  # When c only contains numbers we can send return it
        if int(c) > int(rows):
            return 0
        return int(c)


def print_end(stdscr, length, g):
    stdscr.addstr(14, g.high + 2, "Time it took: " + str(length) + "s", curses.color_pair(2))
    stdscr.addstr(15, g.high + 2, "Do you want to play again?",
                  curses.A_NORMAL + curses.color_pair(2))
    stdscr.addstr(16, g.high + 2, "N, n or q quits",
                  curses.A_NORMAL + curses.color_pair(2))
    stdscr.addstr(17, g.high + 2, "everything else restarts", curses.A_NORMAL + curses.color_pair(2))
    stdscr.refresh()
    y = stdscr.getkey()
    if y in ("q", "Q"):
        return "N"
    else:
        return y


def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.init_pair(2, curses.COLOR_CYAN, -1)
    curses.init_pair(3, curses.COLOR_RED, -1)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(5, curses.COLOR_BLUE, -1)
    curses.init_pair(7, curses.COLOR_GREEN, -1)
    curses.init_pair(8, curses.COLOR_YELLOW, -1)
    curses.init_pair(9, curses.COLOR_RED, -1)
    curses.init_pair(10, curses.COLOR_RED, -1)
    curses.init_pair(16, curses.COLOR_GREEN, curses.COLOR_WHITE)
    y = "y"
    while y not in ("n", "N"):
        curr_x = 0
        curr_y = 0
        stdscr.clear()
        size = welcome(stdscr)
        while size < 4:
            size = welcome(stdscr)
        curses.setsyx(curr_y, curr_x)
        g = Game(n=size)
        g.generate_bombs()
        stdscr.clear()
        print_help(stdscr, g)
        start = time.time()
        g.print_board(stdscr)
        while not g.is_game_over() and not g.win():
            c = stdscr.getkey()
            if c in ("q", "Q"):
                y = "N"
                break
            curr_x, curr_y = do_something(curr_x, curr_y, c, g)
            curses.setsyx(curr_y, curr_x)
            print_help(stdscr, g)
            g.print_board(stdscr)
            stdscr.refresh()
        end = time.time()
        length = round(end - start)
        g.print_board(stdscr)
        stdscr.refresh()
        print_help(stdscr, g)
        if y not in ("n", "N"):
            if g.win():
                print_help(stdscr, g)
                g.print_board(stdscr)
                stdscr.refresh()
                stdscr.addstr(13, g.high + 2 + len("You won!"), "You won!",
                              curses.color_pair(5) + curses.A_BOLD + curses.A_BLINK)
            elif g.loose():
                for r, c in g.bomb_locations:
                    g.board[r][c].open(True)
                    g.board[r][c].exploded()
                g.print_board(stdscr)
                print_help(stdscr, g)
                stdscr.refresh()
                stdscr.addstr(13, g.high + 2 + len("Game Over!"), "Game Over!", curses.A_BOLD + curses.color_pair(3))
            y = print_end(stdscr, length, g)


if __name__ == "__main__":
    rows, columns = os.popen("stty size", "r").read().split()
    curses.wrapper(main)
