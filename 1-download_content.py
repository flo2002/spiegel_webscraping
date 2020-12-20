# import all necessary packages
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import pandas as pd

# read the csv file from the "0-get_link.py" script into a Pandas dataframe
links = pd.read_csv('0-links.csv')

# initializes these lists
full_data = []
backup_data = []

# start an iteration over every link in the csv file
for row in links.index:
    # select the current url
    url = links['Links'][row]

    # download the page and parse it to BeatifulSoup in order to analyze it
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # get the date out of the meta tags
    date = str(soup.findAll('meta')[13])[15:31]
    # filter out the unnecessary characters
    date = date.replace('-', '')
    date = date.replace(':', '')
    date = date.replace('+', '')
    date = date.replace('T', '')

    # get the content of the page
    data = str(soup.findAll('p'))
    # filter for only for the text (And I know ... it could be bettter ;)
    data = re.sub(r'^https?:\/\/.*[\r\n]*', '', data, flags=re.MULTILINE)
    data = data.replace('<p>', ' ')
    data = data.replace('</p>', ' ')
    data = data.replace('.', '')
    data = data.replace('"', '')
    data = data.replace(',', '')
    data = data.replace('-', ' ')
    data = data.replace('\n', ' ')
    data = data.replace('<strong>', ' ')
    data = data.replace('</strong>', ' ')
    data = data.replace('?', '')
    data = data.replace('/', '')
    data = data.replace(':', '')
    data = data.replace('[', '')
    data = data.replace(']', '')
    data = data.replace('href', '')
    data = data.replace('=', ' ')
    data = data.replace('<a>', ' ')
    data = data.replace('<', '')
    data = data.replace('>', '')
    data = data.replace('td', '')
    data = data.replace('tr', '')

    # create a backup dataframe with all the informations
    backup_data = pd.DataFrame({'Index': row, 'Date': date, 'URL': url, 'Data': data}, index=['Index'])
    # sort the dataframe by the date
    backup_data.sort_values(by=['Date'])
    # append it to the "1-backup_data.csv" file
    backup_data.to_csv('1-backup_data.csv', index=False, index_label=row, sep=';', mode='a')

    # append all informations to this list
    full_data.append({'Date': date, 'URL': url, 'Data': data})
    # print the current step
    print(f'{row+1} of {len(links)}')

# convert the list into a dataframe
full_data = pd.DataFrame(full_data)
# sort the dataframe by the date
full_data.sort_values(by=['Date'])
# save the dataframe into the "1-data.csv" file
full_data.to_csv('1-data.csv', index=False, sep=';')
