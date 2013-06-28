#!/usr/bin/python2.7

from unicurses import *

def main():
	stdscr = initscr()
	start_color()
	init_pair(1, COLOR_CYAN, COLOR_BLACK)

	ymax,xmax = getmaxyx(stdscr)

	noecho()
	curs_set(False)
	keypad(stdscr, True)

	addstr("Hello, World!")

	window = newwin(3,xmax,ymax-3,0)
	box(window)
	mvwaddstr(window, 1,1, "I'm here :)")

	panel = new_panel(window)
	update_panels()
	doupdate()
	
	running = True
	while running:
		key = wgetch(window)
		if key == 27:
			running = False

	endwin()

if __name__ == "__main__":
	main()
