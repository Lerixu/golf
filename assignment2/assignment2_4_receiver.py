# -*- coding: utf-8 -*-
"""
Introduction to Web Science
Assignment 2
Question 4
Team : golf

Script description :
    This script declares a 'Receiver' class which will be used as a receiving server
    This script should be run first 
"""

# modules
import socket
import json
import datetime as dt

"""
Receiver class will be able to play the role of a server object 
"""
class Receiver():
    # in the __init__ function we asign a server socket and bind it to the localhost at the port N 8080
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 8080))
        self.server_socket.listen(5)
        
    # the receiv_packet function will be listening to any connection request on the socket and accept it
    # then it reads the packet sent and decode it using the utf8 encoding
    # the decoded packets can then be loaded using json library to rebuild the dictionary
    # the information is the represented in the required format, we also add a timestomp for loging purposes
    def receiv_packet(self):
        c,addr= self.server_socket.accept()
        p=json.loads(c.recv(1024).decode('utf8'))
        print('-----------------------------------------------')
        print('{0} : Information received from {1}' .format(dt.datetime.now(),addr))
        print('-----------------------------------------------')
        print('Name : {0};'.format(p['name']))
        print('Age : {0};' .format(p['age']))
        print('Matrikelnummer: {0}' .format(p['matrikelid']))
        print('-----------------------------------------------')
        c.close()

# Main script to start the server, we create a receiver object first
try:
    receiver = Receiver()
    print('{0} : Server started at localhost:8080 !'.format(dt.datetime.now()))
    
    # using a loop while 1 will keap the server listening to connection attempts
    while 1:
        print('{0} : Stand by' .format(dt.datetime.now()))
        receiver.receiv_packet()
except socket.error as exc:
    print ("Error starting the server on the port 8080 : %s" % exc)