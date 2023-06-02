import contactScraper #py file with all functions


import sys, os
import certifi
import pandas as pd

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

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
    assert type(testTeamURLS) == list
    assert all(isinstance(item, str) for item in testTeamURLS)



def test_getContacts():
    sys.stdout.write("\n")
    assert type(testContacts) == dict
    assert all(isinstance(item, str) for item in testContacts['Team Name'])
    assert all(isinstance(item, str) for item in testContacts['Contact Name'])
    assert all(isinstance(item, str) for item in testContacts['Contact Email'])
    assert all(isinstance(item, str) for item in testContacts['URL'])

def test_makeDF():
    df = contactScraper.makeDF(testTeamURLS[0:5],url,s)
    assert type(df) == pd.core.frame.DataFrame