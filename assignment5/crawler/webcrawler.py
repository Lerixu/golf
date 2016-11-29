# -*- coding: utf-8 -*-
"""
Introduction to Web Science
Assignment 5
Question 2
Team : golf

Script description :
    This script crawls the domain http://141.26.208.82 starting from the
    url : http://141.26.208.82/articles/g/e/r/Germany.html 
    it counts the number of external and internel links on each web pages
    and writes the result into a txt file
"""

import os 
from urllib import parse,request as req,error
import re
import logging 

# we initialize the logging parameter 
logging.basicConfig(filename='webCrawler.log',
                    format='%(asctime)s -  %(levelname)s - %(message)s', 
                    level=logging.DEBUG)
# we clear the lof file and results file for a fresh start
with open('webCrawler.log', 'w'):
    pass

with open('webpage_results.txt', 'w'):
    pass

"""
WebPage class is used to store information about the webpage, 
it inherits from Object class to be able to overide and use __eq__
    link : the url of the page
    valide_link : boolean holding information about link accessibility
    internal_links : a set of WebPage objects for internal links
    nbr_internal_links : hold the number of internal links 
    external_links : a set of WebPage objects for external links
    nbr_external_links : number of external links
"""
class WebPage(object):
    # we initiliaze the default value and log that we are in a new webpage
    def __init__(self,url):
        self.link=url
        self.parsed_link = parse.urlparse(url)
        self.valid_link=True
        self.internal_links=set()
        self.nbr_internal_links= 0
        self.external_links=set()
        self.nbr_external_links= 0
        logging.info('New webpage added : %s'%url)
     
    # function used to store the external and internal links as well as
    # count them
    def stats(self,ext_links,int_links):
        self.internal_links=set(int_links)
        self.nbr_internal_links=len(self.internal_links)
        self.external_links=set(ext_links)
        self.nbr_external_links=len(self.external_links)
        logging.info('webpage {0} has {1} external links and {2} internal links'
                     .format(self.link,self.nbr_external_links,
                             self.nbr_internal_links))
        print('webpage {0} has {1} external links and {2} internal links'
                     .format(self.link,self.nbr_external_links,
                             self.nbr_internal_links))
        
        return self.nbr_external_links,self.nbr_internal_links
    # overiding __str__ to return link
    def __str__(self):
        return self.link
    # overiding __eq__ to compare using link
    def __eq__(self, other): 
        return self.link == other.link
    # implementing hash function on the link
    def __hash__(self):
        return hash(self.link)
        
"""
our WebCrawler class, it initializes a number of global variables to keep
track of the crawled pages.
starting_link : the starting point for our crawler
root_dir : the current working directory
nbr_wpages : the number of webpages crawled (html files)
nbr_external_links : number of external links parsed so far
nbr_internal_links : number of internal links parsed so far
webpage_rslt : the result for each web pages, used later for ploting
"""
class WebCrawler:
    
    def __init__(self,link):
        self.starting_link = link
        self.parsed_link = parse.urlparse(link)
        self.root_dir = os.path.dirname(os.path.realpath(__file__))
        self.nbr_wpages=0
        self.nbr_external_links=0
        self.nbr_internal_links=0
        self.webpage_rslt=''
        
    # we reuse the function to complete the relative urls
    def create_full_url(self,link):
        url = link
        path = self.parsed_link.path
        hostname = "http://"+self.parsed_link.hostname
        if path == "":
            path = "/"
        # absolut path
        if link[0]=="/":
            url = hostname + link
        #fully qualified domain name
        elif len(link) > 7 and link[0:7]=="http://":
            url = link
        # relative path
        else:
            parentfolders = 0
            while len(link)>3 and link[0:3]=="../":
                link = link[3:]
                parentfolders= parentfolders + 1
                url = (hostname + "/".join(path.split("/")
                [0:-(1+parentfolders)])+"/"+link)
        return url 
        
    # split_ext_int_links function allows to return a set of external links
    # and a set of internal links from an array of links
    def split_ext_int_links(self,links):
        ext_links=[]
        int_links=[]
        for l in links:
            # for each link we create a WebPage object
            wp = WebPage(l)
            # checking if it hase the same domain name or not
            if(wp.parsed_link.hostname == self.parsed_link.hostname):
                int_links.append(wp)
            else:
                ext_links.append(wp)
        return ext_links,int_links
        
    # main function for for crawling a giving page
    def crawl_page(self,web_page):
        # we determine the file_name (we decode the path for special characters)
        file_name=self.root_dir+parse.unquote(web_page.parsed_link.path)
        try:
            # attempting to open the url
            res = req.urlopen(web_page.link) 
            # we store the headers received in this variable
            headers = res.info()
            # if the response code is 200
            if(res.getcode() == 200):
                logging.info('webpage %s returned status '\
                             'code 200'%web_page.link)
                # we extract the directory from the file name
                directory = os.path.dirname(file_name)
                # if the directory does not exist we create it
                if not os.path.exists(directory):
                    os.makedirs(directory)
                # we write the content of the filename as bynarie
                with open(file_name,'wb') as of:
                    of.write(res.read())
            # incase we receive a status code diffrent then 200
            else:
                web_page.valid_link=False
                logging.warning('webpage %s is not accessible, '\
                                'returned status code %s'\
                                %(web_page.link,res.getcode()))
                return
            # now we check if the content is an html file
            if(headers['Content-Type'] == 'text/html'):
                # we increment the number of webpages
                self.nbr_wpages+=1
                html=''
                # we extract the encoding used, if no encoding specified
                # we fall on utf8 as its the most common
                encoding_used=headers['charset'] if headers['charset'] else 'utf8'
                # we read the file (not optimal for looping, would be better to
                # store the html in a variable)
                with open(file_name,'rb') as f:
                    html=f.read().decode(encoding_used)
                # we extract all links in 'href' attributes
                links=re.findall(r'href=[\'"]?([^\'" >]+)',html)
                # creating full urls
                full_urls=[self.create_full_url(link) for link in links]
                # spliting the links into external and internal
                elinks,ilinks= self.split_ext_int_links(full_urls)
                # storing the links in the WebPage object 
                nbr_elinks,nbr_ilinks=web_page.stats(elinks,ilinks)
                # appending the results in the webpage_reslt list 
                # we use the ';' as seperator
                self.webpage_rslt+=(web_page.link+';'+\
                                         str(web_page.nbr_external_links)+\
                                         ';'+str(web_page.nbr_internal_links)+'\n')
                self.nbr_external_links+=nbr_elinks
                self.nbr_internal_links+=nbr_ilinks
                return web_page
        except error.URLError as e:
            logging.error('webpage %s not found'%web_page.link) 
        except Exception as e:
            print(e)
            logging.error('webpage %s not accessilbe'%web_page.link) 
            
    # save_results simply writes the final results in 2 files for later use
    def save_results(self):
        # we concatenate the results and use a ';' 
        final_results=self.starting_link+';'+str(self.nbr_wpages)+';'\
            +str(self.nbr_external_links)+';'+str(self.nbr_internal_links)
        with open('final_results.txt','a') as f:
            f.write(final_results)     
        with open('webpage_results.txt','a') as f:
            f.write(self.webpage_rslt) 
        logging.info('Starting page: %s\n Nummber of webpages:%s\n Number '\
                     'of external links:%s\n Number of internal links:%s'\
                     %(self.starting_link,self.nbr_wpages,\
                       self.nbr_external_links,self.nbr_internal_links))
   
    # main  funtion to start the web crawler, it follows a breath first
    # search algorithm by using a set of visited links
    # and an array as of WebPage objects as a queue
    def crawl(self):
        # WebPage object as starting point
        starting_web_page=WebPage(self.starting_link)
        # we initialize the visited WebObject list and the queue
        # this is why we need to overide the __eq__ function
        # since we use mainly the link variable of WebPage for comparison
        visited, queue = set(), [starting_web_page]
        # while there are objects in queue
        while queue:
            # we pop the first element in queue
            wp = queue.pop(0)
            # if its not a visited WebPage we proceed
            if wp not in visited:
                # add the page to the visited links
                visited.add(wp)
                # crawl the page for internal links
                crawled_page=self.crawl_page(wp)
                # the crawled_page return a value if its an html webpage
                # not a media file or other
                if(crawled_page):
                    queue.extend(crawled_page.internal_links - visited)
            if(self.nbr_wpages == 5000):
                break
        # at the end of the crawling process we call the save_results function 
        self.save_results()
        
# we start the program     
logging.info('Starting web crawler')
# Creating a web crawler starting from the given link
web_crawler=WebCrawler('http://141.26.208.82/articles/g/e/r/Germany.html')
# calling the crawl function
web_crawler.crawl()
logging.info('Web crawler finished')
        