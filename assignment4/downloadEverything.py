# -*- coding: utf-8 -*-
"""
Introduction to Web Science
Assignment 4
Question 1
Team : golf

Script description :
    This script reads an html file as input and parses it to retrieve
    all links to image files then calls the 'httpclient' script to download them
"""

# modules
from urllib.parse import urlparse
import sys
import re
import httpclient

"""
main function, takes the name of the html file and the link it was downloaded from
"""
def download(localfile,link):
    parsed_link = urlparse(link)
    # reading from the file
    html_file=open(localfile,'rb')
    # decoding using 'utf8' as it is the most commun encoding used
    # in order to dynamicly know the correct encoding we can probably read the
    # header first, and from the charset value we can deduce the encoding 
    html=html_file.read().decode('utf8')
    # using a regular expression to check for .jpg | gif |png, we also use r'
    # for raw string values, and we tell it to extract the value between quotes
    image_urls=re.findall(r'src=[\'"]?([^\'" >]+.(?:jpg|gif|png))',html)
    html_file.close()
    # we will store the complete urls in this variable after evaluating them
    complete_urls=[]
    # now we need to check for absolute paths
    for url in image_urls:
        # if it starts with http, then its already an absolute path 
        # we check the negative case instead
        if(not url.startswith('http:')):
            # incase it starts with '/' then we need to append the protocol
            # and the domain to the url 
            if(url.startswith('/')) :
                url='http://'+parsed_link.netloc+url
            else:
            # else it means that the resource is in a sub directory of the link
                url=link+url
            complete_urls.append(url)
        else:
            complete_urls.append(url)
    # we print the urls to the console
    print('\n'.join(complete_urls))
    
    # we call the httpclient.http_get function on every url
    for url in complete_urls:
        httpclient.http_GET(url)
        
# we check the number of arguments first (we need 2)
if len(sys.argv) == 3:
    download(sys.argv[1],sys.argv[2])
#    download("introduction-to-web-science","http://west.uni-koblenz.de/en/studying/courses/ws1617/introduction-to-web-science")
else:
    print('Invalid arguments')

    