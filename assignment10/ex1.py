"""
Introduction to Web Science
Assignment 10
Team : golf
exercise 1
"""
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

# we start by reading and processing the data
with open("onlyhash.data", "r",encoding='utf8') as data:
    working_data = []
    for line in data:
        line=line.replace('\n','').split('\t')
        working_data.append(line)
wdata=np.array(working_data)
# we create a dataframe to hold our data
df=pd.DataFrame(data=wdata[:,:],columns=['user','date','tweets'])
print(df.head())
# every tweet contains at least one meme, so we split by ' ' before comparing
def count_meme(meme,tweets):
    cnt=0
    for t in tweets:
        if meme in t.split(" "):
            cnt+=1
    return cnt
# calculate entropy given a list of tweets    
def entropy(tweets):
    N = len(tweets)
    #unique, counts = np.unique(memes, return_counts=True)
    memes=set(meme for t in tweets for meme in t.split(" "))
    counts=[count_meme(meme,tweets) for meme in memes]
    return -sum([C/N*math.log(C/N) for C in counts])
# getting the list of days   
days=df.date.unique()
entropies=[]
# we loop on every day
for day in days:
    # getting a dataframe representing the rows of the current day
    df_day=df.loc[df.date == day]
    # lis of all users that tweeted this day
    users=df_day.user.unique()
    # calculating the system entropy
    system_entropy=entropy(df_day.tweets)
    # calculating the average user entropy 
    avg_user_entropy=sum([entropy(df_day.loc[df_day.user == u].tweets)
                                            for u in users])/len(users)
    entropies.append([system_entropy,avg_user_entropy])

ranked_data=np.array(entropies)
# saving data to a file
np.savetxt("ranked.out",ranked_data,delimiter=',')

# recovering the data
values=np.genfromtxt("ranked.out",delimiter=",")
# we sort ascending using the system entropy column
ranked_data=np.sort(values,axis=0)
# generate all ranks
ranks=[i for i in range(0,len(ranked_data))]
"""
Ploting a ranked plot of the daily system entropy and the average user entropy
"""
system_entropies=ranked_data[:,0]
avg_user_entropies=ranked_data[:,1]
plt.plot(ranks, system_entropies, 'r',label="System entropy")
plt.plot( ranks,avg_user_entropies,"b--",label="Average user entropy")
plt.xlabel("Rank")
plt.ylabel("Entropy")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()

"""
Ploting a scatter plot of system entropy and average user entropy
"""

system_entropies=values[:,0]
avg_user_entropies=values[:,1]

plt.scatter(avg_user_entropies,system_entropies)
plt.xlabel("Average user entropy")
plt.ylabel("System entropy")
plt.xlim(0,0.5)
plt.ylim(0,14)
plt.show()