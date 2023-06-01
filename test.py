import contactScraper
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

s = requests.session()
s.verify = certifi.core.where()

retry = Retry(connect=3, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry)
s.mount('http://', adapter)
s.mount('https://', adapter)

s.keep_alive = False # disable keep alive



url = 'https://norcalpremier.com'
start = '/clubs'

testTeamURLS = contactScraper.getTeamUrls(start,url,s)
testContacts = contactScraper.getContact(url+testTeamURLS[1],s)


def test_greeting():
    contactScraper.greeting()
    sys.stdout.write("\n")


def test_TeamURLs():
    assert len(testTeamURLS) == 5



def test_getContacts():
    sys.stdout.write("\n")
    assert type(testContacts) == 'dict'
    assert len(testContacts) == 4

def test_makeDF():
    df = contactScraper.makeDF(testTeamURLS[0:5],url,s)
    assert type(df) == 'dataframe'


if __name__ == '__main__':
    test_greeting()
    test_TeamURLs()
    test_getContacts()
    test_makeDF()
#test = contactScraper.getTeamUrls()
#testdic = contactScraper.makeDic(test[0:5])
#testdf = contactScraper.makeDF(testdic)