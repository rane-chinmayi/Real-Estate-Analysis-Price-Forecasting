import pandas as pd

df1 = pd.read_csv('C:/Users/chizi/Documents/GitHub/MSIS 5193/Homework/project-deliverable-2-ok-real-estate/data/listings.csv')

df1.shape
df1.columns

null_values = df1.isna()
null_columns = null_values.any()

columns_with_null_values = df1.columns[null_columns].tolist()
print(columns_with_null_values)

df1.dtypes

df1.Price.unique

def clean_price(x):
  if x.startswith('From$'):
    x = x[5:]
    x = x.replace(',','')
    return int(x)
  if x.startswith('$'):
    x = x[1:]
    x = x.replace(',','')
    return int(x)
  else:
    return 0

clean_price('From$12,345')

df1['Price'] = df1['Price'].apply(lambda x: clean_price(x))
#df1.shape
#df1.isna().sum()

df1.shape

df2 = df1[~(df1['Price']==0)]
df2

df2.shape

def clean_address(x):
  x = x.split(' ')
  return x[-1]

#clean_address('Skyline Trails 428 Compass Drive, Mustang, OK 73099')
df2['Zipcode']=df2['Address'].apply(lambda x: clean_address(x))

df2.head

df3 = df2.copy()
#df2.Zipcode.astype(int)
(df3['Zipcode']=='data').sum()

df4 = df3[~(df3['Zipcode']=='data')]

df4.shape

df4.dtypes

df4.Zipcode = df4.Zipcode.astype(int)

df4.dtypes

df4.Sizes.unique()

def clean_size(x):
  sum = 0
  for i in x:
    if i.isdigit():
      sum = sum*10 + int(i)
  return sum

df4['Sizes'] = df4.Sizes.apply(lambda x: clean_size(x))

df5 = df4.copy()

df5.shape
df5.dtypes

df5.Beds.unique()

df5.Beds.fillna(0)

df5.shape

#nan_values = df5[df5['Beds'].isna()]
#len(nan_values)
df5 = df5.dropna(subset=['Beds'])

df5.shape

df5.Beds.unique()

df5.dtypes

df5['Beds'] = df5.Beds.astype(int)

df5.dtypes

df5.head(10)

df5.Baths.unique()

def clean_baths(x):
  if '+' in x:
    x = x.replace('+','')
  return float(x)

clean_baths('12.5+')

df5['Baths'] = df5.Baths.apply(lambda x: clean_baths(x))

df5.head(10)

df5 = df5.drop('Address', axis = True)

df5.shape

df5.dtypes

df5.head(10)

df5.plot.scatter(x='Sizes',
                  y='Price',
                  c='DarkBlue')

df5.shape

df6 = df5[df5['Sizes']<10000]

df6.shape

df6.plot.scatter(x='Sizes',
                  y='Price',
                  c='DarkBlue')


# Data Visualization
import numpy as np

x = df6['Price'].tolist()
X = np.array(x)

y = df6['Sizes'].tolist()
Y = np.array(y)

import matplotlib.pyplot as plt
plt.scatter(y, x, color = 'Blue')
plt.title('House Price')
plt.xlabel('Size')
plt.ylabel('Price')
plt.show()

X = df6.drop(['Price','Zipcode','Beds','Baths'],axis = 'columns')
X

y = df6['Price']
y

import seaborn as sns

sns.heatmap(df6.corr(),annot=True)
#Regression

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=0)

from sklearn.linear_model import LinearRegression
lr = LinearRegression()
lr.fit(X_train,y_train)
lr.score(X_test,y_test)

from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import cross_val_score

cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=0)

cross_val_score(LinearRegression(), X, y, cv=cv)

from sklearn.model_selection import GridSearchCV

from sklearn.linear_model import Lasso
from sklearn.tree import DecisionTreeRegressor

def find_best_model_using_gridsearchcv(X,y):
    algos = {
        'linear_regression' : {
            'model': LinearRegression(),
            'params': {
                'normalize': [True, False]
            }
        },
        'lasso': {
            'model': Lasso(),
            'params': {
                'alpha': [1,2],
                'selection': ['random', 'cyclic']
            }
        },
        'decision_tree': {
            'model': DecisionTreeRegressor(),
            'params': {
                'criterion' : ['mse','friedman_mse'],
                'splitter': ['best','random']
            }
        }
    }
    scores = []
    cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=0)
    for algo_name, config in algos.items():
        gs =  GridSearchCV(config['model'], config['params'], cv=cv, return_train_score=False)
        gs.fit(X,y)
        scores.append({
            'model': algo_name,
            'best_score': gs.best_score_,
            'best_params': gs.best_params_
        })

    return pd.DataFrame(scores,columns=['model','best_score','best_params'])

find_best_model_using_gridsearchcv(X,y)


