import pandas as pd
import os

### extract lat and long from the string

def seperate_lat(latlong):
    res = eval(latlong)
    if res:
        return res['latitude']
    else:
        return 0

def seperate_long(latlong):
    res = eval(latlong)
    if res:
        return res['longitude']
    else:
        return 0

'''
change dollar and M sign in Price
and convert it into int
'''
def clean_sold_price(price):
    temp = str(price)
    if 'M' in temp:
        temp = temp.replace('$', '')
        temp = temp.replace('M', '')
        temp = float(temp)
        return int(temp*1000000)
    else:
        temp = temp.replace('$','')
        temp = temp.replace(',','')
        return int(temp)

df = pd.read_csv('{add your path}/data/scraped_zillow.csv')

#size of the dataframe
print(df.shape)
print(df.dtypes)

# Code to identify the columns containing all the null values
null_values = df.isna()
null_columns = null_values.any()

columns_with_null_values = df.columns[null_columns].tolist()
print(columns_with_null_values)

# Replace numerical coulums with 0 and String with None
# Converting values to int
df[['beds','baths','area']] = df[['beds','baths','area']].fillna(0)

df.beds = df.beds.astype(int)
df.baths = df.baths.astype(int)
df.area = df.area.astype(int)

# Droping columns not required for analysyis
print(df.dtypes)
df = df.drop(columns=['providerListingId', 'imgSrc','hasImage', 'imgSrc','statusType', 'statusText','countryCurrency', 'unformattedPrice',
                 'addressCity', 'addressState','isUndisclosedAddress', 'isZillowOwned','variableData', 'badgeInfo','hdpData', 'isSaved',
                 'isUserClaimingOwner', 'isUserConfirmedClaim','pgapt', 'sgapt','zestimate', 'shouldShowZestimateAsPrice','has3DModel', 'hasVideo',
                 'isHomeRec', 'hasAdditionalAttributions', 'isFeaturedListing', 'availabilityDate', 'list','relaxed',
                 'streetViewURL', 'streetViewMetadataURL', 'lotAreaString', 'info6String','brokerName'
                 ])


# Clean Price of the house
df['price'] = [clean_sold_price(price) for price in df['soldPrice']]
# Drop Rows which have 0 area
empty_row_index = df[df['area'] == 0 ].index
df.drop(empty_row_index , inplace=True)

# create lat and long columns
df['latitude'] = [seperate_lat(latlong) for latlong in df['latLong']]
df['longitude'] = [seperate_long(latlong) for latlong in df['latLong']]

df = df.drop(columns=['soldPrice','latLong','Unnamed: 0'])

# renaming columns
df = df.rename(columns={'addressZipcode': 'Zipcode','beds': 'number of bedrooms','baths': 'number of bathrooms'}, inplace=False)
print(df.dtypes)
df.to_csv('{add your path}/data/placeholder.csv',index=False)