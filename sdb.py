#!/usr/bin/env python

import curses
import curses.panel
import curses.textpad
import string
import time
import hashlib

def rc4(data,key):
	# KSA
	box = list(range(256))
	j = 0
	for i in range(256):
		j = (j + box[i] + ord(key[i % len(key)])) % 256
		box[j],box[i] = box[i],box[j]
	# PRGA
	i = 0
	j = 0
	out = []
	for c in data:
		i = (i + 1) % 256
		j = (j + box[i]) % 256
		box[j],box[i] = box[i],box[j]
		out.append(chr(ord(c) ^ box[(box[i] + box[j]) % 256]))
	return out

def to_string(lst):
	return "".join(lst)

def inputbox(y,x,y0,x0,doEcho):
	box = curses.newwin(y,x,y0,x0)
	box.keypad(True)
	box_panel = curses.panel.new_panel(box)
	curses.panel.update_panels()
	curses.doupdate()
	box.bkgd('_')
	val = ""
	length = 0
	enter = False
	while not enter:
		c = box.getch()
		if c in [ord('\n'),ord('\t'),ord(' ')]:
			enter = True
		elif chr(c) in string.printable and length < x-1:
			if doEcho:
				box.addch(chr(c))
			else:
				box.addch("*")
			length+=1
			val+=chr(c)
		elif (c in [8,127] or c == curses.KEY_BACKSPACE) and length > 0: # BACKSPACE/DELETE
			curry,currx = box.getyx()
			box.delch(curry,currx-1)
			box.addch('_')
			box.move(curry,currx-1)
			length-=1
			val=val[:-1]
	return val

def login(ymax,xmax):
	lymax = 7
	lxmax = 40
	login_str = "LOGIN:"
	username_str = "Username:"
	password_str = "Password:"
	y0 = int((ymax-lymax)/2)
	x0 = int((xmax-lxmax)/2)
	login = curses.newwin(lymax,lxmax,y0,x0)
	login.keypad(True)
	login.border()
	login_panel = curses.panel.new_panel(login)
	curses.panel.update_panels()
	curses.doupdate()
	login.addstr(int(lymax/7),int((lxmax-len(login_str))/2),login_str,curses.A_BOLD)
	login.addstr(int(lymax*3/7),1,username_str)
	login.addstr(int(lymax*4/7),1,password_str)
	username = inputbox(1,lxmax-3-len(username_str),y0+int(lymax*3/7),x0+2+len(username_str),True)
	login.addstr(int(lymax*3/7),2+len(username_str),username)
	password = inputbox(1,lxmax-3-len(username_str),y0+int(lymax*4/7),x0+2+len(password_str),False)
	return (username,password)

def message(mesg,ymax,xmax,y,x):
	lymax = y
	lxmax = x
	y0 = int((ymax-lymax)/2)
	x0 = int((xmax-lxmax)/2)
	msg = curses.newwin(lymax,lxmax,y0,x0)
	msg.keypad(True)
	msg.border()
	msg_panel = curses.panel.new_panel(msg)
	curses.panel.update_panels()
	curses.doupdate()
	msg.addstr(int(3*lymax/7),int((lxmax-len(mesg))/2),mesg,curses.A_BOLD)
	return msg.getch()

def okbox(mesg,ymax,xmax,y,x):
	lymax = y
	lxmax = x
	ok = "[  OK  ]"
	cancel ="[CANCEL]"
	y0 = int((ymax-lymax)/2)
	x0 = int((xmax-lxmax)/2)
	okb = curses.newwin(lymax,lxmax,y0,x0)
	okb.keypad(True)
	okb.border()
	okb_panel = curses.panel.new_panel(okb)
	curses.panel.update_panels()
	curses.doupdate()
	okb.addstr(int(2*lymax/7),int((lxmax-len(mesg))/2),mesg,curses.A_BOLD)
	okb.refresh()
	notDone = True
	qualities = [curses.A_REVERSE,curses.A_NORMAL,curses.A_REVERSE]
	i = 0
	while notDone:
		okb.addstr(int(4*lymax/7),int((2*lxmax/4-len(ok))/2),ok,qualities[i])
		okb.refresh()
		okb.addstr(int(4*lymax/7),int((2*3*lxmax/4-len(cancel))/2),cancel,qualities[i+1])
		okb.refresh()
		k = okb.getch()
		if k == curses.KEY_LEFT and i == 1:
			i = 0
		elif k == curses.KEY_RIGHT and i == 0:
			i = 1
		elif k in [ord('\n'),ord('\r')]:
			notDone = False
	return i
		
	
def main():
	keys = {}
	try:
		keyfile = open("keys.db","r")
		for line in keyfile:
			try:
				uname = line.split(":")[0]
				passd = line.split(":")[1][:-1]
				keys[str(uname)] = str(passd)
			except:
				pass
		keyfile.close()
	except:
		pass
	stdscr = curses.initscr()
	stdscr.keypad(True)
	ymax,xmax = stdscr.getmaxyx()
	curses.noecho()
	try:
		while True:
			username,password = login(ymax,xmax)
			m = hashlib.sha256()
			m.update(password.encode())
			if username in keys.keys() and m.hexdigest() == keys[username]:
				message("Authentication Successful",ymax,xmax,7,40)
			else:
				message("Authentication Failed",ymax,xmax,7,40)
				if not username in keys.keys():
					resp = okbox("New User?",ymax,xmax,11,50)
					if resp == 0:
						keys[username] = m.hexdigest()
						message("User '" + username + "' created",ymax,xmax)
	except:
		pass
	curses.endwin()
	keyfile = open("keys.db","w")
	for user in keys.keys():
		keyfile.write(user + ":" + keys[user] + "\n")
	keyfile.close()

if __name__ == '__main__':
	main()
