"""
Introduction to Web Science
Assignment 5
Question 3
Team : golf

Script used to extract data from the article-per-line file and process it
to finaly write it in a csv file
"""
import pandas as pd
from geonamescache import GeonamesCache
from geonamescache.mappers import country


gc = GeonamesCache() # we use the GeonamesCache to get the name of countries

# creating a mapper between the iso3 code and the country name
mapper = country(from_key='name', to_key='iso3')
countries = list(gc.get_dataset_by_key(gc.get_countries(), 'name',).keys())
# for the US we are going to use the states
states = list(gc.get_us_states_by_names())
#print(countries)
# any of these key words could indicate that we are reading about a star
key_words=['movie','film','TV','television','actor','actress']
articles=[]
dataset={}

with open('article-per-line.txt','r',encoding="utf8") as f:
    articles=f.read().splitlines()


for a in articles:
    dec=a.split('born in',1)
    proceed=True
     # we still need to optimize and factorize our code for this part
    if len(dec) > 1:
        for s in states:
            #print("Looking for %s"%s)
            if(s in dec[1]):
                star=0
                proceed=False
                for k in key_words:
                        if(k in a):
                            star=1
                            break
                country_info=dataset.get('USA')
                
                if(country_info):
                    country_info['count']=country_info['count']+1
                    country_info['star']=country_info['star']+star
                else:
                    dataset['USA']={'name':'United States',
                    'count':1,'star':star}
                break
        if proceed:
            for c in countries:
                #print("Looking for %s"%c)
                if(c in dec[1]):
                    star=0
                    for k in key_words:
                            if(k in a):
                                star=1
                                break
                    country_info=dataset.get(mapper(c))
                    
                    if(country_info):
                        country_info['count']=country_info['count']+1
                        country_info['star']=country_info['star']+star
                    else:
                        dataset[mapper(c)]={'name':c,'count':1,'star':star}
                    break
    
country_ids=[]
frames=[]
for country_iso,d in dataset.items():
    frames.append(pd.DataFrame.from_dict(dict([['code',[country_iso]],
                                               ['name',d['name']],
                                               ['count',[d['count']]]
                                               ,['star',[d['star']]]])))
    
df =pd.concat(frames)
df=df.set_index('code')
df.to_csv('dataset.csv', sep=',', encoding='utf-8')
print(df)