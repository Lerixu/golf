"""
Introduction to Web Science
Assignment 7
Question 3
Team : golf

"""
import matplotlib.pyplot as plt
import numpy as np
import operator
import random
from collections import Counter

# function to roll a fair sided dice
def rollDice():
    # equall probabilty to get a number between 1 and 6 (7 excluded)
    outcome=random.randrange(1,7)
    print(outcome)
    return outcome

# get the CDF from an array    
def getCDF(sums):
    dsums,frequencies=zip(*Counter(sums).most_common())
    cumsum=np.cumsum(frequencies)
    normedcumsum=[x/float(cumsum[-1]) for x in cumsum]
    dsrank = {dsums[i]:i+1 for i in range(0,len(dsums))}
    return dsums,dsrank,frequencies,normedcumsum

# simulate the model taking n as a paramter
def simulation(n):
    sums=[]
    for i in range(n):
        d1 = rollDice()
        d2 = rollDice()
        dsum = d1+d2
        sums.append(dsum)
    return sums

n=1000
sums1=simulation(n)
sums2=simulation(n)

median1 = np.median(sums1)
median2 = np.median(sums2)

mean1 = np.mean(sums1)
mean2 = np.mean(sums2)

"""
Ploting histogram of the first simulation (n=100 or n=1000)
"""
plt.hist(sums1,bins=range(0, 13, 1))
plt.plot([mean1]*len(range(0,160)),range(0,160),"b",label="mean")
plt.plot([median1]*len(range(0,160)),range(0,160),"g",label="median")
plt.ylabel("Frequency")
plt.xlabel("Sum")
plt.title("Dice roll sum frequency for 1st simulation")
plt.xlim(2,12)
plt.legend()
plt.show()

dsums1,dsrank1,frequencies1,normedcumsum1=getCDF(sums1)
dsums2,dsrank2,frequencies2,normedcumsum2=getCDF(sums2)

"""
ploting CDF for both simulations using n = 100 or 1000 
"""
plt.figure()
fig = plt.gcf()
fig.set_size_inches(6,5)
fig.savefig('test2png.png', dpi=100)

r1 = np.arange(1, len(dsums1)+1)
s1 = np.array([float(i) for i in normedcumsum1])

plt.plot(r1, s1, color='green',label='Simulation 1' ,linewidth = 2)

r2 = np.arange(1, len(dsums2)+1)
s2 = np.array([float(i) for i in normedcumsum2])

plt.plot(r2, s2, 
          color='blue',label='Simulation 2',
          linewidth = 2)

plt.grid(True)
plt.xlabel("Sums ")
plt.ylabel("Cumulative probabilities ")
plt.plot([mean1]*len(range(0,2)),range(0,2),"m",label="mean 1")
plt.plot([median1]*len(range(0,2)),range(0,2),"c",label="median 1")
plt.plot([mean2]*len(range(0,2)),range(0,2),"m",label="mean 2",
         linestyle ='dashed')
plt.plot([median2]*len(range(0,2)),range(0,2),"c",label="median 2",
         linestyle ='dashed')

max_distance_1_2=max([abs(x) for x in list(map(operator.sub,
                      normedcumsum1, normedcumsum2))])
#used to store y coordinates 
y12s=[]
x12=0

comun_sums=[val for val in r1 if val in r2]

for r in comun_sums:
    y12=normedcumsum1[r]
    y21=normedcumsum2[r]
    if max_distance_1_2==abs(y12-y21):
        x12=r+1
        y12s.append(y12)
        y12s.append(y21)
        break
    
plt.axvline(x=x12, ymin=min(y12s), ymax=max(y12s), 
            linestyle ='dashed',color='red')
plt.text(x12+1, sum(y12s)/2+0.01,
         'd12 = %.2f'%max_distance_1_2,color='red')

plt.title('CDF Plot ')
plt.xlim(1,13)
plt.legend(bbox_to_anchor=(0, 1 ,1.4, 0),  ncol=1)
plt.show()
print ("Median 1st simulation:",median1)
print ("Mean 1st simulation:",mean1)
print ("Median 2nd simulation:",median2)
print ("Mean 2nd simulation:",mean2)
print ("Maximum distance is :",max_distance_1_2)


