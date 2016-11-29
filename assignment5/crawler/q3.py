# -*- coding: utf-8 -*-
"""
Introduction to Web Science
Assignment 5
Question 3
Team : golf

Script description :
    This scripts read the result file of the previous question and plots
    a histogram and a scatter plot
"""

import numpy as np
import matplotlib.pyplot as plt

# function used to calculate the median
def getmedian(lst):
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // 2
    if (lstLen % 2):
        return sortedLst[index]
    else:
        return (sortedLst[index] + sortedLst[index + 1])/2.0
# function used to draw a histogram          
def draw_hist(data):
    plt.xlim([min(data)-5, max(data)+5])
    plt.hist(data, bins=5, alpha=0.5)
    plt.title('Distribution of links amongs crawled webpages')
    plt.xlabel('Number of webpages')
    plt.ylabel('Number of links')  
    plt.show()     
# function used to plot scatter
def draw_scatter(x,y):
    N = 2 # dimension
    area = np.pi * (15 * np.random.rand(N))**2  # 0 to 15 point radiuses
    plt.scatter(x, y, s=area,  alpha=0.5)
    plt.show()

# recovers our webpage results from the file          
wps=[]
with open('webpage_results.txt', 'r') as f:
    wps = f.read().splitlines()
# splitting using the ';' seperator
# index 0 is the web page, 1 is the number of external links and 
# 2 is the number of internal links
m =np.array(list(wp.split(';') for wp in wps))
# links
x=m[:,0]
# nbr external links per webpage
ey=list((int(k) for k in m[:,1]))
# nbr internal links per webpage
iy=list((int(k) for k in m[:,2]))
# total nbr of links per webpage
data=[a + b for a,b in zip(iy, ey)]
# total number of webpages
total=len(x)
# total umber of links
nbr_links=sum(data)
# average
average=nbr_links/total
# median
median=getmedian(data)
print('Total number of webpages : %s'%total)
print('Total number of links : %s'%nbr_links)
print('Average number of links : %s'%average)

draw_hist(data) 
draw_scatter(iy,ey)

