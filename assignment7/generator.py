"""
Introduction to Web Science
Assignment 7
Question 2
Team : golf

"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import probabilities as dist
import string
import operator
import random
from collections import Counter

#9 function to calculate the cumulative probabilities of a distribution
def generate_cumulative_probs(distribution):
    sorted_keys = sorted(distribution,key=distribution.get)
    cumul_values = np.cumsum(sorted(distribution.values()))
    cumulative_probabilities = dict(zip(sorted_keys, cumul_values))
    return cumulative_probabilities

# sample a random character fom a cumulative distribution
def sampleCharacter(cumul):
    r= random.random()
    x_condidates={}#we store all values > then the random number
    for key, value in cumul.items():
        if value > r:
            x_condidates[key]=value
    # we pick the key of the lowest value
    character = min(x_condidates, key=x_condidates.get)  
    return character

def fetchAllWords(filename):
    f = open(filename,'r',encoding='utf8')
    allWords=[]
    for line in f:
        line = line[:-1]
        words= line.split()
        allWords.extend(words)
    return allWords
    
# returns the ranks, frequencies and normelized cumusum
def getWordStats(filename):
    words,frequencies=zip(*Counter(fetchAllWords(filename)).most_common())
    cumsum=np.cumsum(frequencies)
    normedcumsum=[x/float(cumsum[-1]) for x in cumsum]
    wrank = {words[i]:i+1 for i in range(0,len(words))}
    return words,wrank,frequencies,normedcumsum

""" 
Starting the script
"""
# generating cumulative probabilities
uniform_set=generate_cumulative_probs(dist.uniform_probabilities)
zipf_set=generate_cumulative_probs(dist.zipf_probabilities)

# we are only looking for alphabets and spaces
wanted_chars=list(string.ascii_lowercase)
wanted_chars.append(' ')
# we create a dictionary to store our counts
char_count = dict((x,0) for x in wanted_chars)

# using the artivle per line dump of simple wikipedia
with open('article-per-line.txt','r',encoding="utf8") as f:
    for c in list(f.read()):
        if c in char_count:
            char_count[c] += 1

# sum of all counts
n=sum(char_count.values())

print('Total characters and spaces found = ',n)

# global variable to store our generated uniform dataset
gen_uniform_dataset=''

for i in range(n):
    # we sample n times
    gen_uniform_dataset+=sampleCharacter(uniform_set)
        
with open('uniform_dataset.txt','w') as uf:
    uf.write(gen_uniform_dataset)

gen_zipf_dataset=''

for i in range(n):
    gen_zipf_dataset+=sampleCharacter(zipf_set)
        
with open('zipf_dataset.txt','w') as uf:
    uf.write(gen_zipf_dataset)

# getting the ranks, frequencies and normilzed cumsums for ploting
words_1,wrank_1,frequencies_1,normedcumsum_1=getWordStats('article-per-line.txt')
words_2,wrank_2,frequencies_2,normedcumsum_2=getWordStats('zipf_dataset.txt')
words_3,wrank_3,frequencies_3,normedcumsum_3=getWordStats('uniform_dataset.txt')

"""
ploting word rankings
"""
plt.figure()
r1 = np.arange(1, len(words_1)+1)
f1=np.array([float(i) for i in frequencies_1])

r2 = np.arange(1, len(words_2)+1)
f2=np.array([float(i) for i in frequencies_2])

r3 = np.arange(1, len(words_3)+1)
f3=np.array([float(i) for i in frequencies_3])

# using a loglog plot for readability
plt.loglog(r1, f1, 
          color='darkgreen', 
          linewidth = 2)
plt.loglog(r2, f2, 
          color='darkblue', 
          linewidth = 2)
plt.loglog(r3, f3, 
          color='darkred', 
          linewidth = 2)

text_corupus_patch = mpatches.Patch(color='darkgreen', 
                                    label='Wikipedia corpus')
zipf_corupus_patch = mpatches.Patch(color='darkblue', 
                                    label='Zipf corpora')
uniform_corupus_patch = mpatches.Patch(color='darkred', 
                                       label='Uniform corpora')
plt.legend(handles=[text_corupus_patch,zipf_corupus_patch,
                    uniform_corupus_patch])

plt.grid(True)
plt.xlabel("Word ranks")
plt.ylabel("Frequency")
plt.title('Word ranking plot')

plt.show()

"""
ploting CDF of word ranks
"""

n1=np.array([float(i) for i in normedcumsum_1])

n2=np.array([float(i) for i in normedcumsum_2])

n3=np.array([float(i) for i in normedcumsum_3])

plt.plot(r1, n1, 
          color='darkgreen', 
          linewidth = 2)
plt.plot(r2, n2, 
          color='darkblue', 
          linewidth = 2)
plt.plot(r3, n3, 
          color='darkred', 
          linewidth = 2)

plt.semilogx()#scale only x to log

# we are looking to draw distance lines on plots from each generated model
# to the corpus model
# [NEED_OPTIMIZATION] we calculate the max of all distances
max_distance_1_2=max([abs(x) for x in list(map(operator.sub,
                      normedcumsum_1, normedcumsum_2))])
#used to store y coordinates 
y12s=[]
# rank used
x12=0
# we iterate over each rank, once we find the one giving the maximum distance
# we save it in x12
# NOTE: this part need a more pythonic and optimized solution
# we check using the intersection of ranks between the sets
for r in [val for val in r1 if val in r2]:
    y12=normedcumsum_1[r]
    y21=normedcumsum_2[r]
    if max_distance_1_2==abs(y12-y21):
        x12=r
        y12s.append(y12)
        y12s.append(y21)
        break
plt.axvline(x=x12, ymin=min(y12s), ymax=max(y12s), 
            linestyle ='dashed',color='darkblue')
plt.text(x12+2, sum(y12s)/2+0.05,
         'd12 = %.2f'%max_distance_1_2,color='darkblue')

# we do the same for dataset 1 and 3
max_distance_1_3=max([abs(x) for x in list(map(operator.sub, 
                      normedcumsum_1, normedcumsum_3))])

y13s=[]
x13=0
for r in [val for val in r1 if val in r3]:
    y13=normedcumsum_1[r]
    y31=normedcumsum_3[r]
    if max_distance_1_3==abs(y13-y31):
        x13=r
        y13s.append(y13)
        y13s.append(y31)
        break
plt.axvline(x=x13, ymin=min(y13s), ymax=max(y13s), 
            linestyle ='dashed',color='darkred')
plt.text(x13+2, sum(y13s)/2-0.05, 
'd13 = %.2f'%max_distance_1_3,color='darkred')


text_corupus_patch = mpatches.Patch(color='darkgreen',
                                    label='Wikipedia corpus')
zipf_corupus_patch = mpatches.Patch(color='darkblue',
                                    label='Zipf corpora')
uniform_corupus_patch = mpatches.Patch(color='darkred',
                                       label='Uniform corpora')
plt.legend(handles=[text_corupus_patch,
                    zipf_corupus_patch,uniform_corupus_patch],
                    bbox_to_anchor=(0, 1), loc='upper left', ncol=1)

plt.grid(True)
plt.xlabel("Ranks")
plt.ylabel("Cumulative probabilities")
plt.title('CDF Plot')



plt.show()