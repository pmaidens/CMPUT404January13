#!/usr/bin/env python

#Copyright (c) 2016 Peter Maidens

import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect(("localhost", 12345))

request = "GET / HTTP/1.0\r\n\r\n"

clientSocket.sendall(request)

response = bytearray()
while True:
	part = clientSocket.recv(1024)
	if (part):
		response.extend(part)
	else:
		break

print response

