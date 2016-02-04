#!/usr/bin/env python

"""
Commander.py - Python Backend for the WiFi Pineapple Commander module.

Foxtrot (C) 2016 <foxtrotnull@gmail.com>
"""

import ConfigParser
import os
import sys
from bufferedsocket import BufferedSocket
import string
import time

class Commander(object):
	def __init__(self):
		print "[*] WiFi Pineapple Commander"
		print "[*] Looking for Commander.conf..."
		if os.path.exists('commander.conf'):
			print "[*] Found configuration file!"
			print " "
			self.config = ConfigParser.RawConfigParser()
			self.config.read('commander.conf')
			if self.config.has_section('Network') & self.config.has_section('Commands'):
				print "[*] Valid configuration file... proceeding"
				print " "
			else:
				print "[!] Configuration does not have Network or Command blocks."
				sys.exit(1)
		else:
			print "[!] Could not find configuration file! Exiting..."
			sys.exit(1)

class Client(Commander):
	def __init__(self):
		super(Client, self).__init__()
		self.sock = BufferedSocket()
	def connect(self):		
		server = self.config.get('Network', 'Server')
		port = self.config.getint('Network', 'Port')
		nickname = self.config.get('Network', 'Nickname')
		channel = self.config.get('Network', 'Channel')

		print "[*] Using these connection settings! :"
		print "    Server: " + server
		print "    Port: " + str(port)
		print "    Nickname: " + nickname
		print "    Channel: " + channel
		print " "

		print "[*] Connecting!"
		self.sock.connect(server, port)

		print "[*] Sending nickname and joining " + channel
		self.sock.sendline("NICK %s" % nickname)
		self.sock.sendline("USER %s 8 * :%s" % (nickname, nickname))
		time.sleep(5)
		self.sock.sendline("JOIN %s" % channel)
		self.sock.sendline("PRIVMSG %s :Connected!" % channel)
		print "[*] Connected!"
		print " "
		while True:
			line = self.sock.nextline()
			print repr(line)
			if line.startswith('PING'):
				print "[*] Replying to ping from server"
				self.sock.sendline('PONG %s' % line.split()[1])

			commands = self.config.options('Commands')
			linearr = line.split(' ')
			if len(linearr) >= 4and linearr[3] == 'PRIVMSG':
				message = 'PRIVMSG '.join(line.split('PRIVMSG ')[1:])
				message = ' '.join(message.split(' ')[1:])[1:]
				print '\n'+message+'\n'
				for command in commands:
					if message.startswith(command):
						print "[*] Found command %s" % command

def main():
	client = Client()
	client.connect()

if __name__ == '__main__':
	main()