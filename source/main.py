import curses
import os
import time
from game.Extension import do_something, print_help, welcome, print_end
from game.Game import Game


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
        size = welcome(stdscr, rows)
        while size < 4:
            size = welcome(stdscr, rows)
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
