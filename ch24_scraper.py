#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 17:23:39 2023

@author: Vittom
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 09:46:24 2022

@author: Vitto
"""
#pip install selenium
import sys
import pandas as pd
import csv
import numpy as np
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import time
from time import sleep
import json
import time


## Get link for every page##
link_list = []
for page in range(1, 500, 1):   #possible change in range to include more pages
    option = webdriver.ChromeOptions()
    option.add_argument(" — incognito")
    driver = webdriver.Chrome(executable_path= '/usr/bin/google-chrome-stable %U', chrome_options=option) #'/Library/Application Support/Google/chromedriver', chrome_options=option)
    page_url = "https://www.chrono24.com/rolex/index-" + str(page) + ".htm?resultview=list"
    driver.get(page_url)
    driver.implicitly_wait(10)
    Accept_button = driver.find_element("xpath", "//button[text()[contains(.,'Accept')]]")
    Accept_button.click()

    link =  driver.find_elements("xpath", "//a[contains(@class,'article')]")

    for i in range(len(link)):
        link2 = link[i].get_attribute('href')
        link_list.append(link2)
    
 
##get data in for every link in link_list## 
diz={}
c=1  
#esclusi = [] 
for r in  range(1, len(link_list)):   #possible change in starting number to restart form last obs downloaded
    t0 = time.time()
    option = webdriver.ChromeOptions()
    option.add_argument(" — incognito")
    driver = webdriver.Chrome(executable_path='/Library/Application Support/Google/chromedriver', chrome_options=option)
    driver.get(link_list[r])    
    driver.implicitly_wait(30)
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()[contains(.,'Accept')]]")))
        
    Accept_button = driver.find_element("xpath", "//button[text()[contains(.,'Accept')]]")
    Accept_button.click()
    try:
        WebDriverWait(driver, 15).until(EC.text_to_be_present_in_element((By.XPATH, "//table/tbody[1]/tr/td/strong[1]"), "Listing code"))
        #Aspettiamo fino a che non compare listing code altrimenti i dati inseriti sono nulli
        doc=driver.find_elements("xpath", "//table/tbody/tr/td/h3")
        doc = doc[ : -1]
        prov ={}
        for i in range(len(doc)):
            prov[doc[i].text] = ''
            #del prov[""]
        for j in range(1,len(doc)+1):
            if (doc[j-1].text != 'Functions') and (doc[j-1].text != 'Other'):
                xp_k = '//table/tbody[' + str(j) + ']/tr/td/strong'
                key = driver.find_elements("xpath", xp_k)
                xp_v = '//table/tbody[' + str(j) + ']/tr/td/strong/following::td[1]'
                values = driver.find_elements("xpath", xp_v)
                key_n = []
                values_n = []
                for k in key:
                    key_n.append(k.text)
                for v in values:
                    values_n.append(v.text)
                res = dict(zip(key_n, values_n))
                prov[doc[j-1].text] = res
    
            else:
                el_name = doc[j-1].text
                el_val = "//table/tbody/tr/td/h3[text()[contains(.,'" + el_name + "')]]/following::td[1]"
                res = driver.find_element("xpath", el_val)
                res_list = res.text.split(', ')
                prov[doc[j-1].text] = res_list     
                    
        title = driver.find_element("xpath", "//h1")
        sub_title = driver.find_element("xpath", "//div[contains(@class, 'text-md')]")
        front_price = driver.find_element("xpath", "//span[@class = 'd-block']")
        front = {}
        front['Listing title'] = title.text.split("\n",1)[0]
        front['Listing sub title'] = sub_title.text
        front['Listing price'] = front_price.text
        prov["Title Page"] = front
        
        day = datetime.now().strftime("%d")
        month = datetime.now().strftime("%m")
        year = datetime.now().strftime("%y")
        date = {}
        date["Day"] = day
        date["Month"] = month
        date["Year"] = year
        prov["Date of Download"] = date
        try:
            diz[prov["Basic Info"]["Listing code"]] = prov ####
            t1 = time.time()
            total = t1-t0
            print('watch ' + str(c) + ' in time = ' + str(round(total/60, 2)))
        except:
            print('watch ' + str(c) + 'FAILED')
            #esclusi.append(r)
            pass
    except:
        print('watch ' + str(c) + 'NEVER ENTERED')
        pass
    driver.close()
    c+=1
    


#diz into json  
json_prov = json.dumps(diz, indent = 4)
with open('Finale', 'w') as f:
    f.write(json_prov)
