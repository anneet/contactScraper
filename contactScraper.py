#!/usr/bin/env python
# coding: utf-8



#import json
#import ssl
#from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

import sys, os
import certifi
import pandas as pd
import re
import numpy as np
from collections import defaultdict

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import time
import random

from bs4 import SoupStrainer

from itertools import chain



#ctx = ssl.create_default_context()
#ctx.check_hostname = False
#ctx.verify_mode = ssl.CERT_NONE



#requests.adapters.DEFAULT_RETRIES = 15 # increase retries number

s = requests.session()
s.verify = certifi.core.where()

retry = Retry(connect=3, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry)
s.mount('http://', adapter)
s.mount('https://', adapter)

s.keep_alive = False # disable keep alive



url = 'https://norcalpremier.com'
start = '/clubs'




def decodeEmail(e):
    de = ""
    k = int(e[:2], 16)

    for i in range(2, len(e)-1, 2):
        de += chr(int(e[i:i+2], 16)^k)

    return de



URLext = SoupStrainer("a", href=re.compile("/club/"))
nameStrainer = SoupStrainer(class_="contact-name")
emailStrainer = SoupStrainer(class_="__cf_email__")
teamStrainer = SoupStrainer(class_="team-name")



def getURL(direc,aURL,session): #gets the embedded URLs for a single page
    url = aURL + direc #combine to make full URL

    req= session.get(url,timeout=(2,5))
    content=req.text
    soup=BeautifulSoup(content,'lxml')
    newURLs = {x.get('href') for x in soup.find_all(URLext)} #find all embedded URLs on that page
    return newURLs


def getTeamUrls(direc,aURL,session): #returns all team URLs (teams are within clubs)
    clubs = getURL(direc,aURL,session) #get club URLs (first page URLs)
    total = len(clubs)
    teams = []
    #dic = defaultdict(list)
    sys.stdout.write("Getting Team URLs")
    sys.stdout.write("\n")
    for idx, element in enumerate(clubs):
        sys.stdout.write("\rProgress: %i%%" % np.round((idx/total)*100,2))
        sys.stdout.flush()
        #time.sleep(random.randint(1,4))
        teams += getURL(element,aURL,session) #gets all team URLs for a club page
    sys.stdout.write("\r100% Complete!")
    sys.stdout.write("\n")
    sys.stdout.write("\rTotal teams found: %i" % len(teams))
    return teams

def getContact(teamURL,session): 
    #gets all contact information on a team's page and puts them into a dictionary
    url=teamURL
    req=session.get(url,timeout=(2, 5))
    content=req.text
    soup=BeautifulSoup(content,'lxml')

    details = {'Team Name':[],'Contact Name':[],'Contact Email':[], 'URL':[]}
    rawEmail=soup.findAll(emailStrainer)
    rawName =soup.findAll(nameStrainer)
    teamName = soup.find(teamStrainer)

    for name, email in zip(rawName,rawEmail):
        details['Contact Name'].append(name.text.strip())
        details['Team Name'].append(teamName.text.strip())
        details['URL'].append(url)
        details['Contact Email'].append(decodeEmail(email['data-cfemail'])) #decodes email
    return details




def makeDic(teamURLs,aURL):
    dic = defaultdict(list)
    sys.stdout.write("Getting contact information")
    sys.stdout.write("\n")
    sys.stdout.write("Please wait...")
    sys.stdout.write("\n")
    counter = 0
    for idx,node in enumerate(teamURLs):
        try:
            for k, v in getContact(aURL+node,s).items():
                dic[k].append(v)
                counter += len(dic['Contact Name'])
                sys.stdout.write("\rParsing team %i out of %i. Number of contacts is now %i" % (idx+1, len(teamURLs), counter))
                time.sleep(random.randint(1,4))
        except:
            sys.stdout.write("\n")
            random_sleep_except = random.uniform(240,360)
            print("I've encountered an error! I'll pause for " +str(np.round(random_sleep_except/60)) + " minutes and try again \n")
            time.sleep(random_sleep_except) #sleep the script for x minutes and....#
            print('Okay time to continue!')
            continue
    sys.stdout.write("\n")
    sys.stdout.write("\rAll contacts parsed")
    sys.stdout.write("\n")
    return dic



def makeDF(dic):
    for k in dic.keys():
        dic[k] = list(chain(*dic[k]))
    return pd.DataFrame.from_dict(dic)




def greeting():
    sys.stdout.write("\n")
    sys.stdout.write("Hello! This program has 3 steps")
    sys.stdout.write("\n")
    sys.stdout.write("1.URL gathering")
    sys.stdout.write("\n")
    sys.stdout.write("2.Contact parsing ")
    sys.stdout.write("\n")
    sys.stdout.write("3.Exporting ")
    sys.stdout.write("\n")
    sys.stdout.write("Because of the large amount of contacts, this may take a while and I may need to take a few breaks in between ")
    sys.stdout.write("\n")
    sys.stdout.write("I'll let you know when the breaks occur. Now let's get to work! ")
    sys.stdout.write("\n")



#test = getTeamUrls()
#testdic = makeDic(test[0:5])
#testdf = makeDF(testdic)
#testdf




def main():
    greeting()

    teamURls = getTeamUrls(start,url,s)

    sys.stdout.write("\n")
    random_sleep_except = random.uniform(240,360)
    print("Pausing for " +str(np.round(random_sleep_except/60)) + " seconds. Thank you! \n")
    time.sleep(random_sleep_except/60)
    print("Time to continue")

    dic = makeDic(teamURls,url)
    df = makeDF(dic)
    sys.stdout.write("\rChecking for duplicates...")
    df = df.drop_duplicates(subset=['Team Name','Contact Name',	'Contact Email'	])
    sys.stdout.write("\rDone")
    sys.stdout.write("\n")

    sys.stdout.write("\n")
    sys.stdout.write("\rExporting to xlsx file to folder labeled")
    newpath = os.path.abspath("exports") 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    
    path = os.path.abspath("exports/TeamContacts.xlsx")
    df.to_excel(path)
    sys.stdout.write("\rComplete! Thank you for your patience.")




if __name__ == '__main__':
    main()