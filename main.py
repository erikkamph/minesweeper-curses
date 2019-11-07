import curses
import os
import random
from curses.textpad import Textbox, rectangle


class Cell:
    def __init__(self):
        self.hasBomb = False
        self.hasExploded = False
        self.flagged = False
        self.is_opened = False
        self.neighbours = 0

    def set_flagged(self, b):
        self.flagged = b

    def is_flagged(self):
        return self.flagged

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
        cells = self.board[y]
        if not cells[x].is_flagged():
            cells[x].set_flagged(True)
        self.board[y] = cells

    def print_board(self, stdscr):
        for x in range(self.high):
            for y in range(self.high):
                c = self.get_char(y, x)
                stdscr.addstr(x, y, c, curses.A_NORMAL)

    def get_char(self, x, y):
        cells = self.board[y]
        if cells[x].is_flagged():
            return "F"
        elif cells[x].has_opened():
            if cells[x].hasExploded:
                return "*"
            return str(cells[x].neighbours)
        else:
            return "O"

    def generate_bombs(self):
        for i in range(0, 10):
            self.place_bomb()
        self.neighbours()

    def place_bomb(self):
        r = random.randint(0, (self.high - 1))
        c = random.randint(0, (self.high - 1))
        if self.board[c][r].is_a_bomb():
            self.place_bomb()
        else:
            self.board[c][r].set_is_bomb(True)

    def reveal(self, x, y):
        self.board[y][x].open(True)
        if self.board[y][x].is_a_bomb():
            self.board[y][x].exploded()
        if self.board[y][x].is_flagged():
            self.board[y][x].set_flagged(False)
        if self.board[y][x].neighbours is 0:
            self.open_all_zeros()

    def neighbours(self):
        for row in range(0, (self.high - 1)):
            for col in range(0, (self.high - 1)):
                self.board[row][col].neighbours = self.calc_neighbours(row, col)
                print(self.board[row][col].neighbours)

    def calc_neighbours(self, row, col):
        i = 0
        if (row - 1) > -1:
            if col - 1 > -1:
                if self.board[row-1][col-1].is_a_bomb():
                    i += 1
            if col + 1 < self.high - 1:
                if self.board[row-1][col+1].is_a_bomb():
                    i += 1
            if self.board[row-1][col].is_a_bomb():
                i += 1
        if col - 1 > -1:
            if self.board[row][col-1].is_a_bomb():
                i += 1
        if col + 1 < self.high - 1:
            if self.board[row][col+1].is_a_bomb():
                i += 1
        if self.high > row + 1:
            if col - 1 > -1:
                if self.board[row+1][col-1].is_a_bomb():
                    i += 1
            if self.board[row+1][col].is_a_bomb():
                i += 1
            if col + 1 < self.high - 1:
                if self.board[row+1][col+1].is_a_bomb():
                    i += 1
        return i

    def open_all_zeros(self):
        for x in range(0, self.high - 1):
            for y in range(0, self.high - 1):
                if self.board[x][y].neighbours is 0:
                    self.board[x][y].open(True)


def do_something(x, y, c, g):
    new_x = x
    new_y = y
    n = g.high
    if c in ("a", "A"):
        if x > 0:
            new_x -= 1
    elif c in ("s", "S"):
        if y < (n - 1):
            new_y += 1
    elif c in ("d", "D"):
        if x < (n - 1):
            new_x += 1
    elif c in ("w", "W"):
        if y > 0:
            new_y -= 1
    elif c in ("q", "q"):
        g.isGameOver = True
    elif c in ("f", "F"):
        g.put_flag(x, y)
    elif c in ("r", "R"):
        g.reveal(x, y)
    return new_x, new_y


def print_help(stdscr):
    text = "Movement: "
    w = "w - go up one step"
    a = "a - go left one step"
    s = "s - go down one step"
    d = "d - go right one step"
    f = "f - flag current position"
    r = "r - open current position"
    q = "q - quit the program"
    longest = len(f)
    from_right = int(columns) - longest
    stdscr.addstr(0, from_right, text, curses.A_BOLD)
    stdscr.addstr(1, from_right, w, curses.A_NORMAL)
    stdscr.addstr(2, from_right, a, curses.A_NORMAL)
    stdscr.addstr(3, from_right, s, curses.A_NORMAL)
    stdscr.addstr(4, from_right, d, curses.A_NORMAL)
    stdscr.addstr(5, from_right, f, curses.A_NORMAL)
    stdscr.addstr(6, from_right, r, curses.A_NORMAL)
    stdscr.addstr(7, from_right, q, curses.A_NORMAL)
    curr_y, curr_x = curses.getsyx()
    stdscr.addstr(8, from_right, "Current position:", curses.A_BOLD)
    stdscr.addstr(9, from_right, "X: " + str(curr_x + 1), curses.A_NORMAL)
    stdscr.addstr(10, from_right, "Y: " + str(curr_y + 1), curses.A_NORMAL)


def print_info(stdscr, g):
    g.print_board(stdscr)
    print_help(stdscr)


def welcome(stdscr):
    string = "Enter a size to use for the board:"
    startx = int(int(columns) / 2) - len(string)
    starty = int(int(rows) / 2) - 2
    stdscr.addstr(starty-1, startx+2, string)
    stdscr.addstr(starty+3, startx+2, "Help to the right")
    stdscr.addstr(starty+4, startx+2, "Board on the left")
    editwin = curses.newwin(1, len(string), starty+1, startx+1)
    rectangle(stdscr, starty, startx, starty + 1 + 1, startx + len(string) + 2)
    stdscr.refresh()
    box = Textbox(editwin)
    box.edit()
    return int(box.gather())


def main(stdscr):
    curr_x = 0
    curr_y = 0
    size = welcome(stdscr)
    curses.setsyx(curr_y, curr_x)
    g = Game(size)
    g.generate_bombs()
    stdscr.clear()
    print_info(stdscr, g)
    while g.is_game_over() is False:
        c = stdscr.getkey()
        curr_x, curr_y = do_something(curr_x, curr_y, c, g)
        stdscr.clear()
        curses.setsyx(curr_y, curr_x)
        print_info(stdscr, g)
        stdscr.refresh()


if __name__ == "__main__":
    rows, columns = os.popen("stty size", "r").read().split()
    curses.wrapper(main)
