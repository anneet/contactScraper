
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





def main():
    contactScraper.greeting()

    teamURls = contactScraper.getTeamUrls()

    sys.stdout.write("\n")
    random_sleep_except = random.uniform(240,360)
    print("Pausing for " +str(np.round(random_sleep_except/60)) + " seconds. Thank you! \n")
    time.sleep(random_sleep_except/60)
    print("Time to continue")

    dic = contactScraper.makeDic(teamURls)
    df = contactScraper.makeDF(dic)
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


