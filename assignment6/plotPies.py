"""
Introduction to Web Science
Assignment 5
Question 3
Team : golf

Script used to read the csv file and plot pie charts representing the data
"""
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import cm
import numpy as np

filename = 'dataset.csv'
cols = ['code','count','star','name']
df = pd.read_csv(filename,  usecols=cols)
#print(df)
df.set_index('code', inplace=True)
#df.drop('USA', inplace=True)
total=sum(df['count'])
# make a square figure and axes
plt.figure(1, figsize=(6,6))
ax = plt.axes([0.1, 0.1, 0.8, 0.8])
cs=cm.Set1(np.arange(40)/40.)
# The slices will be ordered and plotted counter-clockwise.
labels = [n if (v/total >0.05) else '' for n, v in zip(df.index, df['count'])]
fracs = [(k/total) for k in df['count']]

def my_autopct(pct):
    return ('%.2f%%' % pct) if pct > 5 else ''
    
patches, texts, autotexts = ax.pie(fracs,  labels=labels,
                autopct=my_autopct,colors=cs,  startangle=90)

plt.title("Geographic distribution of famous people's origin\
 (simple wikipedia)", bbox={'facecolor':'0.8', 'pad':5})
plt.show()


# make a square figure and axes
plt.figure(2, figsize=(6,6))
ax = plt.axes([0.1, 0.1, 0.8, 0.8])

labels = ['Movie/TV stars','Other']
fracs = [df.at['USA','star']/(df.at['USA','count']+df.at['USA','star']),
         df.at['USA','count']/(df.at['USA','count']+df.at['USA','star'])]

patches, texts, autotexts = ax.pie(fracs,  labels=labels,
                autopct='%.2f%%',colors=cs,  startangle=90)
plt.title('Percentage of movie/TV stars in USA (simple wikipedia)', 
          bbox={'facecolor':'0.8', 'pad':5})
plt.show()
