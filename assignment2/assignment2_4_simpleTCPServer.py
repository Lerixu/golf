# -*- coding: utf-8 -*-
"""
Introduction to Web Science
Assignment 2
Question 4
Team : golf

Script description :
    This script creates a simple TCP server listening to a client
"""
# modules
import socket

#we create a connection-oriented sockets (stream socket) that uses TCP
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#we bind it to localhost:8080
tcp_server_socket.bind(('localhost', 8080))
tcp_server_socket.listen(5)
#we listen and accept incoming connections
c,addr= tcp_server_socket.accept()
#we read received data (as a packet of 1024)
print(c.recv(1024))