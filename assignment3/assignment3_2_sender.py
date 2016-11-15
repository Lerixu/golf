# -*- coding: utf-8 -*-
"""
Introduction to Web Science
Assignment 3
Question 2
Team : golf

Script description :
    This script declares a 'Sender' class which will be used as a client
"""

# modules
import socket

"""
the Sender class will play the role of a client object
"""
class Sender():

    # nothing special to initialise for this object
    def __init__(self):
        pass
        
    # the send_packet function allows the Sender objec to send a message to the server
    # First we create a socket, then we attempt to connect to the server
    # we encode the message so we can send it as a byte stream
    # After sending the packet we close the used socket
    def send_packet(self,message):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(('localhost',8080))
            self.socket.send(message.encode('utf8'))
            self.socket.close()
            print('The URL have been sent to the server!')
        except socket.error as exc:
            print ("Error sending data to locolhost:8080 : %s" % exc)
       
    # client function prepares the url and sends it through the socket using the send_packet function
    # the chain argument allows subsequent use of the client if the user wishes to
    def client(self,chain='y'):
        if chain=='y':
            print('-----------------------------------------------')
            print('Sending  URL : http://www.example.com:80/path/to/myfile.html?key1=value1&key2=value2#InTheDocument')
            self.send_packet('http://www.example.com:80/path/to/myfile.html?key1=value1&key2=value2#InTheDocument \r \n')
            self.chain_query()
            
    # chain_query prompts the user for input regarding the client, if he wishes to reuse the client he needs to inpu 'y'
    def chain_query(self):
        input_chain=input('Retry?(y/n) ').strip()
        if input_chain == 'y' or input_chain =='n':
            self.client(input_chain)
        else:
            print('Please provide an answer with y or n')
            self.chain_query()
            

# main script to start the client, we create a sender object and call the client function
sender = Sender()
sender.client()