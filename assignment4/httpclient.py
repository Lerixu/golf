# -*- coding: utf-8 -*-
"""
Introduction to Web Science
Assignment 4
Question 1
Team : golf

Script description :
    This script takes a url as an argument and downloads the resource, 
    separating the header from the content as 2 files
"""

# modules
import socket
from urllib.parse import urlparse
import sys

"""
Seperate_header function is used to split the received binary 
into header and content(body), we keep the document as binary to be able 
to correctly save images 
"""
def seperate_header(document):
    # spliting using the b'\r\n\r\n' as separator
    # we know that after the header there is always a '\r\n\r\n' 
    # before the start of the body
    header,content=document.split(b'\r\n\r\n',1)
    return header,content

"""
receiv_data will retrieve any data from the url as binary
"""
def receiv_data(url):
    # we use the urlparse function to retreive specific info on the url
    parsed_url = urlparse(url)
    path = parsed_url.path
    # we correcte the path incase its empty
    if path == "":
        path = "/"
    # the domaine will be the HOST used for the socket
    HOST = parsed_url.netloc
    # the path represents the ressource to retreive via GET request
    GET = path
    PORT = 80 # default http port
    # variable used to store the received data
    document=b''
  
    try:
        # Creating a TCP streaming socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # We allow the socket to to bind to a port on TIME_WAIT, this is
        # to reduce the 'address already in use' error while downloading in bulk
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((HOST, PORT))
        # sending an HTTP GET request for the resource in the path,
        # requiring a 200 ok response, encoding as 'utf8' to stream binary
        s.send(("GET %s HTTP/1.0 200 OK\r\n\r\n"%GET).encode('utf8'))
        # we keap looping on the receive function using 1024 buffer until 
        #♦ no more data is received, this ensures that all data is received
        while True:
            data = (s.recv(1024))
            if not data:
                break
            document+=data
        s.shutdown(1)
        s.close()
    except socket.error as exc:
        print ("Error sending HTTP GET request: %s" % exc)
    return document
  
"""
function used to read a variable number of files
"""
def read_files(*files):
        for f in files:
            with open(f,'rb') as file:
                print(file.read().decode('utf8'))
        
"""
the http_get function calls the other function in a sequence to correctly 
retrieve the data and split it, then write both the header and the content
in 2 separate files
"""
def http_GET(url):
   
    document = receiv_data(url)
    header,content=seperate_header(document)
    # we split the url using '/' and get the last element as file name
    # this will deal dynamicly with any ressource having extension (.png...)
    file_name=url.split('/')[-1]
    # we append '.header' to the file name so we can store it on a diffrent name
    # we also open the file as 'write binary' 
    header_file = open(file_name+'.header','wb')
    header_file.write(header)
    header_file.close()
    content_file = open(file_name,'wb')
    content_file.write(content)
    content_file.close()
    # we read the header file to the console
    read_files(file_name+'.header')

"""
Main script, it check the number of arguments giving to the script
if it has 1 other argument then call the http_get function
"""
if len(sys.argv) == 2:
    http_GET(sys.argv[1])
else:
    print('Invalid argument, httpclient requires a valid URL')