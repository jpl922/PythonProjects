# -*- coding: utf-8 -*-
"""
Created on Sat May 29 00:07:51 2021
Web scraping with Selenium webdriver  based on tutorial repo
https://www.byperth.com/2018/04/25/guide-web-scraping-101-
what-you-need-to-know-and-how-to-scrape-with-python-selenium-webdriver/
Functions similar to beautifulsoup another common process
@author: Jason @jpl922
"""

# allow the browser to be launched
from selenium import webdriver
# allow search with parameters
from selenium.webdriver.common.by import By
# allow waiting for browser to load
from selenium.webdriver.support.ui import WebDriverWait
# determine is page loaded
from selenium.webdriver.support import expected_conditions as EC
# handling page timeouts
from selenium.common.exceptions import TimeoutException

import pandas as pd


driver_option = webdriver.ChromeOptions()
driver_option.add_argument("-incognito")
# drag files into the terminal to get the path very useful
chromedriver_path = 'C:/Users/17jlo/Desktop/PythonCode/chromedriver.exe'

# def used to create function in python
# in this case a function to create the web driver 
def create_webdriver():
    return webdriver.Chrome(executable_path = chromedriver_path, chrome_options = driver_option)




# opening the website 

browser= create_webdriver()
# get: value of the item is returned 
browser.get("https://github.com/collections/machine-learning")


# Run then inspect element on the website to be able to determine relevant
# information on the site 

# any element on a page can be selected with Xpath 
# Xpath cheatsheet: https://devhints.io/xpath

# extract all projects from the page (there is a locate element html)

projects = browser.find_elements_by_xpath("//h1[@class = 'h3 lh-condensed']")


# extract relevant data from the projects 

project_list = {}

# notice no end statement the end is based on indentation in the code
for proj in projects: 
    proj_name = proj.text # Project name 
    proj_url = proj.find_elements_by_xpath("a")[0].get_attribute('href') # URL
    # look up the brackets in python for indexing 
    project_list[proj_name] = proj_url 

# x.text: etract raw text from element x
# x-get_attributes('y')- extract the value in attribute y from element x


# Close connection 
browser.quit()

# Extracting data

project_df = pd.DataFrame.from_dict(project_list, orient = 'index' )


# Manipulating the Table (data frame)
