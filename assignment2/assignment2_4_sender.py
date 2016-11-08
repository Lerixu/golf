# -*- coding: utf-8 -*-
"""
Introduction to Web Science
Assignment 2
Question 4
Team : golf

Script description :
    This script declares a 'Sender' class which will be used as a client
"""

# modules
import socket
import json

"""
the Sender class will play the role of a client object
"""
class Sender():

    # nothing special to initialise for this object
    def __init__(self):
        pass
        
    # the send_packet function allows the Sender objec to send a message to the server
    # First we create a socket, then we attempt to connect to the server
    # The message is dumped using json library and encoded in utf8 to be sent trough the socket
    # After sending the packet we close the used socket
    def send_packet(self,message):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(('localhost',8080))
            self.socket.send(json.dumps(message).encode('utf8'))
            self.socket.close()
            print('Thank you {0}, your information have been sent to the server.'.format(message['name']))
        except socket.error as exc:
            print ("Error sending data to locolhost:8080 : %s" % exc)
       
    # The client function allows to prompt the use for input and prepare a message
    # to send through the socket using the send_packet function
    # the chain argument allows subsequent use of the client if the user wishes to
    def client(self,chain='y'):
        if chain=='y':
            name=''
            age=''
            matrikelid=''
            print('-----------------------------------------------')
            print('Please provide the following informations :')
            print('*All fields are required!')
            while not(self.field_validation(name)):
                name=input('Name : ').strip()
            
            while not(self.field_validation(age,True)):
                age=input('Age : ').strip()
                
            
            while not(self.field_validation(matrikelid)):
                matrikelid=input('Matrikelnummer : ').strip()
                
            message = {'name':name,'age':age,'matrikelid':matrikelid}
            self.send_packet(message)
            self.chain_query()
            
    # chain_query prompts the user for input regarding the client, if he wishes to reuse the client he needs to inpu 'y'
    def chain_query(self):
        input_chain=input('Retry?(y/n) ')
        if input_chain == 'y' or input_chain =='n':
            self.client(input_chain)
        else:
            print('Please provide an answer with y or n')
            self.chain_query()
            
    # field_validation function allows the client to validate the input
    def field_validation(self,field,is_numeric=False):
        if len(field) ==0:
            return False
        elif is_numeric:
            if field.isdigit():
                return True
            else:
                print('Please provide a valid number')
                return False
        else :
            return True

# main script to start the client, we create a sender object and call the client function
sender = Sender()
sender.client()