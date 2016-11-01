# -*- coding: utf-8 -*-
"""
Introduction to Web Science
Assignment 1

Team : golf
"""

# modules
import random
import math
import matplotlib.pyplot as mplot

# variables

#Array to store the 10 random numbers between 0 and 90
randomSample = []

#Arrays to store the values of sine and cosine on the sample
sin = []
cosin = []

#1. Generate a random number sequence of 10 values between 0 to 90
#initializing the sample
randomSample =  random.sample(range(0,90),10)
print("The random sample used is : %s" %randomSample)

#2. Perform Sine and Cosine operation on numbers generated
#3. Store the values in two different arrays named SIN & COSIN respectively
#calculating the sine 
sin = [math.sin(i) for i in randomSample]
print("Applying sine to the sample : %s" %sin)

#calculating the cosine
cosin = [math.cos(i) for i in randomSample]
print("Applying cosine to the sample : %s" %cosin)

#4. Plot the values of SIN & COSIN in two different colors
#ploting sin in red and cosin in yellow
mplot.plot(randomSample, sin,'r',label="Calculated sine")
mplot.plot(randomSample,cosin,'b',label="Calculated cosine")

#5. The plot should have labeled axes and legend.
mplot.ylabel('Calculated value')
mplot.xlabel('Sample')
mplot.grid(True)

#legend properties
mplot.legend(bbox_to_anchor=(0,1.01,1,0),loc=3, ncol=1, mode="expand", borderaxespad=0)
mplot.show()