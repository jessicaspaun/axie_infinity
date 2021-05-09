import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import re
import time
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

print("ready to scrape")


no_pages = 2

def get_data(pageNo):  
    #headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    r = requests.get('https://axieinfinity.com/','html_parser')#, proxies=proxies)
    time.sleep(10)
    content = r.content
    soup = BeautifulSoup(content)
    print(soup.prettify())
    print("FINISHED WITH SOUP")

    alls = []
    usd = 1
    for d in soup.findAll('div', attrs={'id':'_next'}):
    	print("HELLO D")
    	print(d)
    	name = d.find('div', attrs={'class':'h-0 pb-24 flex flex-row flex-wrap justify-center overflow-hidden items-baseline'})
    	# n = name.find_all('img', alt=True)
    	#print(n[0]['alt'])
    	usd = d.find('h6', attrs={'class':'truncate ml-8 text-gray-1 font-medium'})
    	print(usd)

        # all1=[]

        # if name is not None:
        #     #print(n[0]['alt'])
        #     all1.append(n[0]['alt'])
        # else:
        #     all1.append("unknown-product")

        # if author is not None:
        #     #print(author.text)
        #     all1.append(author.text)
        # elif author is None:
        #     author = d.find('span', attrs={'class':'a-size-small a-color-base'})
        #     if author is not None:
        #         all1.append(author.text)
        #     else:    
        #         all1.append('0')

        # if rating is not None:
        #     #print(rating.text)
        #     all1.append(rating.text)
        # else:
        #     all1.append('-1')

        # if users_rated is not None:
        #     #print(price.text)
        #     all1.append(users_rated.text)
        # else:
        #     all1.append('0')     

        # if price is not None:
        #     #print(price.text)
        #     all1.append(price.text)
        # else:
        #     all1.append('0')
        # alls.append(all1)    
    return usd

get_data(no_pages)