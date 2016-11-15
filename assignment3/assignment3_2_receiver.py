# -*- coding: utf-8 -*-
"""
Introduction to Web Science
Assignment 3
Question 2
Team : golf

Script description :
    This script declares a 'Receiver' class which will be used as a receiving server
    This script should be run first 
"""

# modules
import socket
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
    # we feed the received message to the defined class URL_object and call the function parse_url
    # we call the print_detail function of the url_object to print the information in the required format
    def receiv_packet(self):
        c,addr= self.server_socket.accept()
        p=c.recv(2048).decode('utf8')
        print('-----------------------------------------------')
        print('{0} : Information received from {1}' .format(dt.datetime.now(),addr))
        print('-----------------------------------------------')
        print('\n URL: {0}'.format(p))
        url_object=URLobject()
        url_object.parse_url(p)
        url_object.print_detail()
        c.close()
"""
URL_object is a class that will hold the url values and provide the function 
to parse the url
"""
class URLobject:
    # we initialise all the member variables by N/A which will be printed 
    # in case the url doesnt have one of the elements 
    def __init__(self):
        self.protocol='N/A'
        self.domain='N/A'
        self.sub_domain='N/A'
        self.port='N/A'
        self.path='N/A'
        self.parameters='N/A'
        self.fragment='N/A'
    
    # print_detail simply prints the memeber variables in the required format
    def print_detail(self):
        print('----------------URL Details----------------------')
        print(' Protocol : {0} \n'.format(self.protocol))
        print(' Domain : {0} \n'.format(self.domain))
        print(' Sub-Domain : {0} \n'.format(self.sub_domain))
        print(' Port number : {0} \n'.format(self.port))
        print(' Path : {0} \n'.format(self.path))
        print(' Parameters : {0} \n'.format(self.parameters))
        print(' Fragment : {0} \n'.format(self.fragment))
        print('-----------------------------------------------')
        
    """
    Our main function, it takes a url_string as an argument and parses it.
    We use split function on multiple separators to get the information we are after;
    The concept is to continuously split the url in 2 each time using a separator,
    the first element splited is generaly what we are looking for next,
    the second element splited is then splited in turn in 2 and we repeat the process
    in adition, every time before spliting, we check if the remaining string
    contains the sperator we are using next
    
    we are also taking in consideration the absence of certain element from the url
    for example: the port number can be absent, so is the parameters and fragment
    The function should be able to parse any valid url
    """
    def parse_url(self,url_string):
        # checks if the url contains the ':' separator
        if(':' in url_string):
            # we split the url in 2, giving us the protocol as a fist element
            s1_url = url_string.split(':',1)
            self.protocol = s1_url[0]
            # we will store the domaine part of the url in this variable
            d_url=''
            # we will store the path, parameters and fragment part of the url 
            # in this variable
            s3_url=''
           
            """
            from here we check if there is a second ':' separator indicating 
            the existance of a port number in the url, it its the case 
            we continue spliting using that separator, if the port is absent
            we move to the next separator to get the domain url and the rest
            """
            # we check if the 1st remaining sub-url contains another ':' 
            if(':' in s1_url[1]):
                # we split the 1st sub-url in 2, the first element contains 
                # the domain and subdomain
                s2_url=s1_url[1].split(':',1)
                d_url=s2_url[0]
                # we check the 2nd element of the 2nd sub-url 
                # for any '/' separator
                if('/' in s2_url[1]):
                    # we split  once using the '/' separator, 
                    # this isolates the port number
                    _url=s2_url[1].split('/',1)
                    self.port=_url[0]
                    s3_url = _url[1]
                
                else:
                    # incase there is no '/' separator we consider whats left to be
                    # the port number
                    self.port=s2_url[1]

            # else if there is no port number, we continue spliting to get the domain
            elif ('/' in (s1_url[1])[2:]):
                # we skip the first 2 characters as they are both '/' 
                # then we split by '/' once
                s2_url=(s1_url[1])[2:].split('/',1)
                # the first element contains the domain
                d_url=s2_url[0]
                # the second element conatains whats left of the url
                s3_url=s2_url[1]
            else:
                # if no '/' separator is found, this means that whats left is 
                # the domain and subdomain part of the url
                d_url=(s1_url[1])[2:]
                
            # now we parse the d_url containing the domain part of the url
            # we check if any '.' separator exists
            if( '.' in d_url):
                # we split the 1st element of the 2nd sub-url in 3
                # we consider that we should have 2 '.' separator in most cases
                site_url = d_url.split('.',3)
                # the first 2 elements from the left are 
                # the top level domain and the domain
                self.domain = site_url[-2]+'.'+site_url[-1]
                # the remaining element is the subdomain, 
                # we remove the extra '/'
                self.sub_domain = site_url[-3].replace('/','')
            else:
                # if the domain part of the url does not contain any '.'
                # it is not a valid url
                print(' Not a valid url')
                
            # we check the remaining sub url for any '?' separator
            if('?' in s3_url):
                # we split using '?' separator to get 
                # the path as a first element
                s4_url=s3_url.split('?',1)
                self.path='/'+s4_url[0]
                # we check the remaing sub-url for any '#'
                if( '#' in s4_url[1]):
                    # we split the sub-url using the '#' separator 
                    # to get the parameters as first element and 
                    # fragment as second element
                    s5_url=s4_url[1].split('#',1)
                    self.parameters=s5_url[0].split('&')
                    self.fragment=s5_url[1]
                else:
                    # in this case, this means that the url has no fragment
                    self.parameters=s4_url[1].split('&')
            else:
                # in this case, this means the url has no parameters
                # but might have a fragment
                # we check the remaing sub-url for any '#'
                if('#' in s3_url):
                    # we split the sub-url using the '#' separator 
                    # to get the parameters as first element and 
                    # fragment as second element
                    s4_url=s3_url.split('#',1)
                    self.path='/'+s4_url[0]
                    self.fragment=s4_url[1]
                elif len(s3_url) > 0:
                    # in this case, this means the url has neither parameters nor fragments
                    # whats left is the path
                    self.path='/'+s3_url

            
        else:
            # in the absence of a protocole, the url is not valid
            print(' Not a valid url')
            
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