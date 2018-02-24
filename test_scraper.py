# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 06:26:51 2017

@author: andreas
"""

import requests
from bs4 import BeautifulSoup
from newspaper import Article
import re
import time
import pandas as pd
import numpy as np
import sys

country = [0]
country = "England"

def get_links(country):
    
    country = country.replace(" ","+")
    
    compile_search = "https://www.google.co.uk/search?q=" + country + "&source=lnms&tbm=nws"
   
    page = requests.get(compile_search)
    soup = BeautifulSoup(page.content)
    found_link = list()
    for link in soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
        
        
        url_clean = re.split(":(?=http)",link["href"].replace("/url?q=",""))
                
        found_link.extend(url_clean)
        
        found_link[len(found_link)-1] = re.split("&",found_link[len(found_link)-1])[0]

        
    found_link = list(set(found_link)) # remove duplicates
        
    return found_link

def get_article(url_name):
    
    article_page = Article(url = url_name)
    article_page.download()
    article_page.parse()
    article_text = article_page.text
    
    return article_text

df = pd.DataFrame()

n_scraps =  range(0,10)
    
time_stamp = int(round(time.time()))
    
found_links = get_links(country)
            
adict = []
            
for link in range(0,len(found_links)):
                
    txt = get_article(found_links[link])
                
    new = {'country': country,'timestamp': time_stamp, 'article_txt': txt}
                
    adict.append(new)
                
df = pd.concat([df,pd.DataFrame(adict)],axis=0)
            
sys.stdout.write("{0}>".format("--"))
        
sys.stdout.flush()
       
print "\n" + country + " done"     
time_int = int(round(abs(np.random.normal(loc=18.0, scale=6.0, size=None)) + (np.random.rand() * 10)))
time.sleep(time_int)   
            
valid_articles=list(map(lambda x: len(x.split()) > 200,df["article_txt"].values))
            
df=df.iloc[valid_articles]

df.reset_index(drop=True,inplace=True)
            
            
                
                

