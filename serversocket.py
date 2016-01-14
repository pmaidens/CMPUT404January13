#!/usr/bin/env python

#Copyright (c) 2016 Peter Maidens

import socket
import os
import sys
import select

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverSocket.bind(("0.0.0.0", 12346))

serverSocket.listen(5)

while True:
	print "Waiting for connections"
	(incomingSocket, address) = serverSocket.accept()

	print "We got a connection from %s" % (str (address))

	pid = os.fork()

	if (pid == 0):
		#We must be in child process

		outgoingSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		outgoingSocket.connect(("www.google.com", 80))

		request = bytearray()
		while True:
			incomingSocket.setblocking(0)
			outgoingSocket.setblocking(0)
			try:
				part = incomingSocket.recv(1024)
			except socket.error as exception:
				if exception.errno == 11:
					part = None
				else:
					raise
			if (part):
				request.extend(part)
				outgoingSocket.sendall(part)
			try:
				part = outgoingSocket.recv(1024)
			except socket.error as exception:
				if exception.errno == 11:
					part = None
				else:
					raise
			if (part):
				incomingSocket.sendall(part)

			select.select([incomingSocket, outgoingSocket],
				[],
				[incomingSocket, outgoingSocket])

		print request
		sys.exit(0)
	else:
		#We must be in parent process
		pass
	