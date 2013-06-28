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

	i = 0
	for letter in range(ord('A'),ord('Z')+1):
		exec("window" + str(i) + " = newwin(3,7,i,3*i)")
		exec("box(window" + str(i) + ")")
		exec("mvwaddstr(window" + str(i) + ",1,1, '" + chr(letter) + "')")
		exec("panel" + str(i) + " = new_panel(window" + str(i) + ")")
		update_panels()
		doupdate()
		i += 1

	i-=1	
	running = True
	while running:
		key = getch()
		if key == 27:
			running = False
		elif key == ord('i'):
			if i > 0:
				i-=1
				exec("top_panel(panel" + str(i) + ")")
		elif key == ord('k'):
			if i < 25:
				i+=1
				exec("top_panel(panel" + str(i) + ")")
		update_panels()
		doupdate()

	endwin()

if __name__ == "__main__":
	main()
