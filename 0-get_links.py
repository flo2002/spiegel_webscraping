# import all necessary packages
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import pandas as pd

# initialize the list where all the links will be saved
links = []

# iterate over all 500 pages
for i in range(500):
    # set the url of the category
    url = 'https://www.spiegel.de/international/p' + str(i) + '/'
    if i == 0:
        url = 'https://www.spiegel.de/international/'

    # download the page and parse it to BeatifulSoup in order to analyze it
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # iterate over all links in this page
    for link in soup.findAll('a', attrs={'href': re.compile("https://")}):
        # filter for the starting of the url
        if link.get('href').startswith('https://www.spiegel.de/international/'):
            # if the url is not too short, it will be written in the list
            if len(link.get('href')) > 80:
                links.append({'Links': link.get('href')})

    # prints the status
    print(f'Page: {i+1} of 500')

# converts the list into a Pandas dataframe
links = pd.DataFrame(links)
# drops all duplicate links
links.drop_duplicates(subset='Links', inplace=True)
# save it to a csv file
links.to_csv('0-links.csv', index=False)
