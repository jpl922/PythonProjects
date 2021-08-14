# -*- coding: utf-8 -*-
"""
Created on Sat May 29 12:19:09 2021
Webscraping using beautifulsoup and based on tutorial from github
https://medium.com/@nishantsahoo/which-movie-should-i-watch-5c83a3c0f5b1
example is from:
https://realpython.com/beautiful-soup-web-scraper-python/
@author: Jason @jpl922
"""

# Best practices with webscraping
# 1: make it iterative and no hard coding; versatile code
# 2: make it compliant with robots.text and term and conditions
# 3: do not overburden the website: do not slow it down 
# 4: Use an API if there is a data download API use it (even if fee)
import urllib3
from bs4 import BeautifulSoup

# Basic usage of Beautiful Soup
# end result is printing the title of the website 
bballurl = "https://www.basketball-reference.com/teams/PHI/2021.html"
ourUrl = urllib3.PoolManager().request('GET',bballurl).data
soup = BeautifulSoup(ourUrl,"lxml")
print(soup.find('title').text)


# accessing a particular HTML tag wi/ specific atributes in BS
# look at the first dive for class and upper 
htmleEle = soup.find('div', attrs = {'class': 'upper'}) 

# review findChildren and findall(list of html elements of same type)
#https://www.crummy.com/software/BeautifulSoup/bs4/doc/ official docs


