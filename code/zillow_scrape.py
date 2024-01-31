# This file is scraping data from zillow.com
# It is a dynamic website, users would post information of houses for selling, renting, etc.
# We are focusing on recent sold houses in Stillwater.
# This dataset will include more than 3000 records.

# import packages
from select import select
from numpy import bytes_
import pandas as pd


# These packages are used mainly for scraping data.
# Dr. Hammer shared with me some links that may be helpful for solving problem related to verifying human
# According to these links, I got some ideas of scraping data without open websites by web drivers.
# The data is generated from an external source via API.
# And also stored in script as JSON format, within an HTML comment.
# That's the reason we can easily pull all the data.
import requests
import re
import json
import response

# get data from JSON method
def getDataFromZillow(swo_url):
    swo_url = requests.get(swo_url, headers={'User-Agent': 'Mozilla/5.0'})
    data = json.loads(re.search(r'!--(\{"queryState".*?)-->', swo_url.text).group(1))

    # scrape data for the first page
    for item in data['cat1']['searchResults']['listResults']:
        print(item)

    # write a csv file for the first page
    df = pd.DataFrame.from_dict(data['cat1']['searchResults']['listResults'])
    return df


# create a list to store scraped data
dfs=[]
for i in range(20):
    # write a for loop to access pages' urls
    url_first = "https://www.zillow.com/stillwater-ok/sold/"    
    url_second = ""
    url_third = "?p?searchQueryState=%7B%22pagination"

    # for the first page
    if i == 0:
        print('---------------------------------------{i}-----------------------------',i)
        swo_url = url_first + url_third
        print(swo_url)
        df = getDataFromZillow(swo_url)
        dfs.append(df)

    # for the rest of pages
    else:
        print('---------------------------------------{i}-----------------------------',i)
        url_second = str(i+1)+'_p/'
        swo_url = url_first + url_second + url_third
        print(swo_url)
        df = getDataFromZillow(swo_url)
        dfs.append(df)
result = pd.concat(dfs)
result.to_csv('scraped_data.csv')
# try to scrapie for one page

url_1 = 'ttps://www.zillow.com/stillwater-ok/sold/'

swo_url = requests.get('https://www.zillow.com/stillwater-ok/sold/20_p/?p/',headers = {'User-Agent':'Mozilla/5.0'})
print(swo_url.text)

data = json.loads(re.search(r'!--(\{"queryState".*?)-->', swo_url.text).group(1))


# scrape data for the first page
for item in data['cat1']['searchResults']['listResults']:
    print(item)
    print("")

# write a csv file for the first page
df = pd.DataFrame.from_dict(data['cat1']['searchResults']['listResults'])
print(df)