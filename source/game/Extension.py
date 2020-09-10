import curses
from curses.textpad import Textbox, rectangle
import re


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


def welcome(stdscr, rows):
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