"""
Introduction to Web Science
Assignment 8
Team : golf

"""
import pandas as pd
import re #used for some text cleaning
from collections import Counter
import math
import time # might need to replace by timeit
store = pd.HDFStore('store2.h5')
df1=store['df1']
df2=store['df2']
# number of documents or articles
nbr_docs=len(df1.index)
# we create a new column containing the article words
# we apply a function to remove ponctuation and some other characters for 
# better word set, we also transform the text to lowercase
# column mainly used to calculate term frequencie
df1['words']=df1.text.apply(lambda x: 
    re.sub(r'[,;.\[\]():\*\"\']*','',x).lower().split())
# we also add another column for a set of unique words, column used for jaccard
df1['set']=df1.words.apply(lambda x: set(x))

# function used to calculate the jaccardCoef between 2 wordsets
def calcJaccardSimilarity(wordset1, wordset2):
    # excpetion handling to deal with missing data (inducing division by zero)
    try:
        return len(wordset1.intersection(wordset2))/len(wordset1.union(wordset2))
    except:
        return 0
# the jaccard coef for article 'Germany' and 'Europe'
jaccard_EU_DE=calcJaccardSimilarity(df1[df1.name=="Germany"].iloc[0]['set'],
                                    df1[df1.name=="Europe"].iloc[0]['set'])
print("Jaccard Coef for articles 'Germany' and 'Europe' = %s"%jaccard_EU_DE)

# we create a new column to store term frequencies
df1['frequencies']=df1.words.apply(lambda x: Counter(x))
# variable to store document frequencies
doc_frequencies=dict()
for terms in df1.frequencies.tolist():
    for term in terms:
        if term in doc_frequencies:
            doc_frequencies[term] += 1
        else:
            doc_frequencies[term] = 1

# function used to calculate the tfidf
def calculateTFIDF(tf,df):
    return tf*math.log(nbr_docs/df)

# function used to build a dictionary of tfidf    
def buildTFIDFdict(frequencies):
    tfidfDict=dict()
    for term in frequencies:
        tfidfDict[term]=calculateTFIDF(frequencies[term],doc_frequencies[term])
    return tfidfDict

# function used to calculate the euclidian distance based on the tfidf    
def docEuclidDist(tfIdfDict):
    return math.sqrt(sum([math.pow(value,2) for key,value in tfIdfDict.items()]))

# adding tfidf column to store the tfidf-dictionaries    
df1['tfidf']=df1.frequencies.apply(lambda x: buildTFIDFdict(x))
# we also store the euclidian distance for future use
df1['euclid']=df1.tfidf.apply(lambda x: docEuclidDist(x))

# function used to calculate cosine similarity, we added 2 more parameters
# euclid1 and euclid2 so we can feed our already calculated distances
def calculateCosineSimilarity(tfIdfDict1, tfIdfDict2,euclid1,euclid2):
        # will hold the product of tfidfs
        product_vars=[]
        for term in tfIdfDict1:
            if(term in tfIdfDict2):
                product_vars.append(tfIdfDict1[term]*tfIdfDict2[term])
        sum_=sum(product_vars)
        # non Null vectors
        if(sum_ != 0 and euclid1 != 0 and euclid2 != 0):
            return math.acos(sum_/(euclid1*euclid2))
        else:
            # in case of a null vector we return a pie number 
            # will need to think of a better solution
            return 3.14
# calculating cosine similarity between article 'Germany' and 'Europe'
theta=calculateCosineSimilarity(df1[df1.name=="Germany"].iloc[0]['tfidf'],
                                df1[df1.name=="Europe"].iloc[0]['tfidf'],
                                df1[df1.name=="Germany"].iloc[0]['euclid'],
                                df1[df1.name=="Europe"].iloc[0]['euclid'])
print("Cosine similarity between article 'Germany' and 'Europe' is = %s"%theta)

# applying the jaccardSimilarity function on the outlinks
jaccard_EU_DE_outlinks=calcJaccardSimilarity(set(df2[df2.name=="Germany"].\
                                                 iloc[0]['out_links']),
                            set(df2[df2.name=="Europe"].iloc[0]['out_links']))

print("The jaccard graph coef of articles 'Germany' and 'Europe' = %s"
      %jaccard_EU_DE_outlinks)

#storing a new dataframe for later use
#store['df1_c']=df1

# function used to rank aticles from most similar 
# takes an article as input and 2 dataframes
# calculates 3 measures using the 3 implemented methods
def queryArticles(article,df1_sub,df2_sub):
    # selecting the query article row in both dataframes
    df1_article=df1[df1.name==article].iloc[0]
    df2_article=df2[df2.name==article].iloc[0]
    # will hold jaccard similarity ranked articles
    jsim_ranks=dict()
    # will hold cosine similarity ranked articles
    cosim_ranks=dict()
    # will hold jaccard graph similarity ranked articles
    jsimgraph_ranks=dict()
    
    for index, row in df1_sub.iterrows():
        # we skip if its the same article as the one in the query
        if(row['name'] != article):
            # calculating using the jaccard and cosine similarity (dataframe 1)
            jsim_ranks[row['name']]=calcJaccardSimilarity(df1_article['set'],
                                                                    row['set'])
            cosim_ranks[row['name']]=calculateCosineSimilarity(
                                             df1_article['tfidf'],
                                                     row['tfidf'],
                                            df1_article['euclid'],
                                                    row['euclid'])
    
    for index, row in df2_sub.iterrows():
        if(row['name'] != article):
            # calculating using the jaccard graph similarity (dataframe 2)
            jsimgraph_ranks[row['name']]=calcJaccardSimilarity(
                        set(df2_article['out_links']),set(row['out_links']))
    
    # sorting using the rank value
    sorted_jsim_ranks=sorted(jsim_ranks.items(),
                                     key=lambda x: x[1],reverse=True)
    sorted_cosim_ranks=sorted(cosim_ranks.items(),
                                      key=lambda x: x[1])
    sorted_jsimgraph_ranks=sorted(jsimgraph_ranks.items(),
                                          key=lambda x: x[1],reverse=True)
    
    return sorted_jsim_ranks,sorted_cosim_ranks,sorted_jsimgraph_ranks

# calling the query function on article "Germany"    
sorted_jsim_ranks,sorted_cosim_ranks,\
                        sorted_jsimgraph_ranks=queryArticles("Germany",df1,df2)
# printing the 5 most similar articles given per method
print("**Applying a query on article 'Germany'\n")
print("*Fetching top 5 most similar articles per measure\n")
print(" Jaccard similarity top 5: \n%s\n"%sorted_jsim_ranks[0:4])
print(" Cosine similarity top 5: \n%s\n"%sorted_cosim_ranks[0:4])
print(" Jaccard graph similarity top 5: \n%s\n"%sorted_jsimgraph_ranks[0:4])




# we will use the Kendall rank correlation coefficient method to compare
# our 3 similarity measures
# takes as parameter the article, the calculated dataframe and a pair of measures
def calculateKendallTau(article,df_sim,m1,m2):
    # selecting the subject row
    df_row=df_sim[df_sim.name==article].iloc[0]
    # extracting the names from the sorted results of the first measures
    # this is important as it helps with calculation if the first method is
    # ranked properly from highest to lowest rank, and so we use the sorted
    # articles from the first measure to loop on the second measure
    names=[t[0] for t in df_row[m1]]
    # total number of ranks
    ranks=len(names)
    m2_ranks=[]
    # appending the proper rank of each article
    for n in names:
        m2_ranks.append(getRankFromTupleList(df_row[m2],n))
    
    c=[]# ordered list of number of concordant pairs
    d=[]# ordered list of number of discordant pairs
    # for each rank we check the value with the next ranks
    # if its higher we increment the concordant number
    # if its lower we increment the discordant number
    # we skip counting the last rank as there is no rank below it
    for i in range(0,ranks-1):
        c_cnt=0
        d_cnt=0
        for j in range(i,ranks-1):
            if m2_ranks[j]>m2_ranks[i]:
                c_cnt+=1
            else:
                d_cnt+=1
        c.append(c_cnt)
        d.append(d_cnt)
    sum_c=sum(c)
    sum_d=sum(d)
    # summing up and calculating tau
    return (sum_c-sum_d)/(sum_c+sum_d)

# calculating the average tau for random 100 strategie
print("**Random 100 article strategie results : \n")

# strategie 1
#100 random articles

df1_random_sample=df1.sample(100)
df2_random_sample=df2[df2.name.isin(df1_random_sample.name)]
                      
#print(df1_sample,df2_sample)

# function used to get an index value from a tuple list
# will be used to get the rank of a specific article
def getRankFromTupleList(l,value):
    for pos,t in enumerate(l):
        if(t[0] == value):
            return pos+1
# creating new dataframe to hold the experiment results            
df_ = pd.DataFrame(columns=['name','jaccard','cosim','jgraph'])
rows=[]
ts = time.time()
# applying the query for each article and creating a series for it
for article in df1_random_sample.name:
    jsim,cosim,jgraph=queryArticles(article,df1_random_sample,df2_random_sample)
    rows.append(pd.Series({'name': article,
                        'jaccard': jsim,
                        'cosim': cosim,
                        'jgraph': jgraph}))
ts1=time.time()-ts
print("Computing similarity using 3 methods for 100 article in %s seconds\n"%ts1)
print("Computing %s articles could be estimated to last : %s seconds\n"%(nbr_docs,nbr_docs/100*ts1))
# series are appended to the dataframe as rows    
df_=df_.append(rows)
# in case of 'jaccard' vs 'cosine'
ttau_random_jc=0
for a in df1_random_sample.name:
    ttau_random_jc+=calculateKendallTau(a,df_,'jaccard','cosim')
average_tau_random_jc=ttau_random_jc/(len(df1_random_sample.name)-1)
print(" The average Kendall Tau for 'jaccard' vs 'cosine' is %s"
      %average_tau_random_jc)

ttau_random_jjg=0
for a in df1_random_sample.name:
    ttau_random_jjg+=calculateKendallTau(a,df_,'jaccard','jgraph')
average_tau_random_jjg=ttau_random_jjg/(len(df1_random_sample.name)-1)
print(" The average Kendall Tau for 'jaccard' vs 'jaccard graph' is %s"
      %average_tau_random_jjg)

ttau_random_cjg=0
for a in df1_random_sample.name:
    ttau_random_cjg+=calculateKendallTau(a,df_,'cosim','jgraph')
average_tau_random_cjg=ttau_random_cjg/(len(df1_random_sample.name)-1)
print(" The average Kendall Tau for 'cosine' vs 'jaccard graph' is %s\n"
      %average_tau_random_cjg)

# calculating the average tau for longest 100 strategie
print("**Longest 100 article strategie results : \n")
# applying a lenght function on text column and sorting using it
df1=df1.assign(l = df1.text.apply(lambda x : len(x))).sort_values(
                                                        'l',ascending=False)
# we sample the top 100 longest articles
df1_longest_sample=df1[0:99]
df2_longest_sample=df2[df2.name.isin(df1_longest_sample.name)]
              
# we create a new dataframe for our second experiment                       
df_2 = pd.DataFrame(columns=['name','jaccard','cosim','jgraph'])
rows_2=[]
for article in df1_longest_sample.name:
    jsim,cosim,jgraph=queryArticles(article,df1_longest_sample,df2_longest_sample)
    rows.append(pd.Series({'name': article,
                        'jaccard': jsim,
                        'cosim': cosim,
                        'jgraph': jgraph}))
df_2=df_2.append(rows)
                       
# in case of 'jaccard' vs 'cosine'
ttau_longest_jc=0
for a in df1_longest_sample.name:
    ttau_longest_jc+=calculateKendallTau(a,df_2,'jaccard','cosim')
average_tau_longest_jc=ttau_longest_jc/(len(df1_longest_sample.name)-1)
print(" The average Kendall Tau for 'jaccard' vs 'cosine' is %s"
      %average_tau_longest_jc)

ttau_longest_jjg=0
for a in df1_longest_sample.name:
    ttau_longest_jjg+=calculateKendallTau(a,df_2,'jaccard','jgraph')
average_tau_longest_jjg=ttau_longest_jjg/(len(df1_longest_sample.name)-1)
print(" The average Kendall Tau for 'jaccard' vs 'jaccard graph' is %s"
      %average_tau_longest_jjg)

ttau_longest_cjg=0
for a in df1_longest_sample.name:
    ttau_longest_cjg+=calculateKendallTau(a,df_2,'cosim','jgraph')
average_tau_longest_cjg=ttau_longest_cjg/(len(df1_longest_sample.name)-1)
print(" The average Kendall Tau for 'cosine' vs 'jaccard graph' is %s\n"
      %average_tau_longest_cjg)

                    