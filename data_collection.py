import requests
import pandas as pd
from bs4 import BeautifulSoup

# Get Html and create Soup
r = requests.get('https://twitter.com/realDonaldTrump?lang=en-gb')
soup = BeautifulSoup(r.content, "lxml")
