# After we tried visualizing the data from zillow.com, we found that it did not looks like linear.
# That means we would have difficulty in using linear regression, which we thought is one of important analysis.
# Thus, we discussed and decided to change the data source.
# The new data were scraped from realtor.com, which is also a real estate website for buying/renting/selling houses.

# imput packages
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

prices = []
beds = []
baths = []
sizes = []
addresses = []
final_lst = []
driver = webdriver.Firefox()

# The new data is focusing on sold houses on realtor.com
# Again, we used method of Beautifulsoup
def pull_data(i):
    url = 'https://www.realtor.com/realestateandhomes-search/Oklahoma-City_OK'+'/pg-'+str(i)
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, features='html.parser')
    # Find the attributes in CSS selector
    for element in soup.findAll('li', attrs={'class': 'component_property-card'}):
        price = element.find('span', attrs={'data-label': 'pc-price'})
        bed = element.find('li', attrs={'data-label': 'pc-meta-beds'})
        bath = element.find('li', attrs={'data-label': 'pc-meta-baths'})
        size = element.find('li', attrs={'data-label': 'pc-meta-sqft'})
        address = element.find('div', attrs={'data-label': 'pc-address'})

        # There might be some houses losing data.
        # So, we used if-else to distinguish and return existing data and null data
        if bed and bath:
            nr_beds = bed.find('span', attrs={'data-label': 'meta-value'})
            nr_baths = bath.find('span', attrs={'data-label': 'meta-value'})

            if nr_beds:
                beds.append(nr_beds.text)
            else:
                beds.append('')
            if nr_baths:
                baths.append(nr_baths.text)
            if price and price.text:
                prices.append(price.text)
            else:
                prices.append('No data')

            if size and size.text:
                sizes.append(size.text)
            else:
                sizes.append('No data')

            if address and address.text:
                addresses.append(address.text)
            else:
                addresses.append('No data')

    df = pd.DataFrame({'Address': addresses, 'Price': prices, 'Beds': beds, 'Baths': baths, 'Sizes': sizes})
    final_lst.append(df)



for i in range(2,87):
    pull_data(i)
    print(f'{i} over')


dfx = pd.concat(final_lst)
len(dfx)
dfx.to_csv('listings.csv', index=False, encoding='utf-8')
