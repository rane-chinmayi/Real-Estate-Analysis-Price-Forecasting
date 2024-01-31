# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

df = pd.read_csv('realtor.csv')
df = df.drop_duplicates(ignore_index=True)
#df= df[df['Sizes']<10000]
df = df[~(df['Beds']==0)]
df = df[~(df['Sizes']==0)]
#df = df[~(df['Beds']==24)]

df.shape

df.sha

df2 =df[df['Beds']==0]
df2

df.plot.scatter(x='Sizes',
                  y='Price',
                  c='DarkBlue')

df['Beds'].value_counts().sort_index(ascending=True).plot(kind='bar')
plt.title('Number of Bedrooms')
plt.xlabel('Bedroom')
plt.ylabel('House')
sns.despine

df2 = df[df['Beds']==7]
df.Beds

plt.title('Number of Bathrooms')
plt.xlabel('Bathroom')
plt.ylabel('House')
sns.countplot(x=df["Baths"])



plt.title('Average Price vs Number of Bedrooms')
plt.xlabel('Beds')
plt.ylabel('Price')
plt.ticklabel_format(style='plain', axis='y')
plt.xticks('Beds')
sns.lineplot(data=df, x="Beds", y="Price")

cl = (df.groupby(['Beds', 'Price'], as_index=False).mean()
            .groupby('Beds').mean())
cl

# Bathroom Line chart
c = df.groupby('Baths')[['Price']].mean().reset_index()
plt.xlabel('Baths')
plt.ylabel('Price')
col_list = c["Baths"].values.tolist()
price_list = c["Price"].values.tolist()
plt.ticklabel_format(style='plain', axis='y')
plt.title('Average Price vs Number of Bathrooms')
listOf_Xticks = np.arange(1, 35, 2)
plt.plot(col_list, price_list)
plt.xticks(listOf_Xticks)


plt.show()

sns.lineplot(data=c, x="Beds", y="Price")



#scatter plot Price vs Size
plt.scatter(df.Price,df.Sizes)
plt.title('Price vs Size')

#scatter plot Price vs Beds
plt.scatter(df.Price,df.Beds)
plt.title('Price vs Beds')

#scatter plot Price vs Baths
plt.scatter(df.Price,df.Baths)
plt.title('Price vs Baths')

#scatter plot Price vs Zipcode
plt.scatter(df.Price,df.Zipcode)
plt.title('Price vs Zipcode')