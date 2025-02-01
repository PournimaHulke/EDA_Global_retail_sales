# import libraries

import numpy as np
import pandas as pb
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

from matplotlib.pyplot import figure
from pandas import value_counts
from unicodedata import category

# load the data
print("Load The Data")
df=pb.read_csv("D:\\Download\\global_retail_sale.zip")
print(df)

#overview/data cleaning                                       # it gives memory usage, datatype
print("Procedure Of Data Cleaning")

print(df.columns)
"""'Order ID', 'Order Date', 'Product ID', 'Product Category',
       'Buyer Gender', 'Buyer Age', 'Order Location', 'International Shipping',
       'Sales Price', 'Shipping Charges', 'Sales per Unit', 'Quantity',
       'Total Sales', 'Rating', 'Review'"""


print("Dataset Information")
print(df.info())


print("Missing Value")
print(df.isnull().sum())

for col in df.select_dtypes(include=['number']):          #object ----> mode
    df[col].fillna(df[col].mean())


print("Duplicated Values")
print('duplicated values',df.duplicated().sum())
print('duplicated values in order id',df['Order ID'].duplicated().sum())


print("drop duplicates")
print(df.drop_duplicates())

#change the datatype
print("")
print("Date Datatype Datetime")
df["Order Date"]=df["Order Date"].astype("datetime64[ns]")
print(df.info())


                                                              # statistical data
print("describe")                                               #describe gives min max 25% 50%
print(df.describe())
print(df.info())


#EDA

print(df.columns)
"""'Order ID', 'Order Date', 'Product ID', 'Product Category',
       'Buyer Gender', 'Buyer Age', 'Order Location', 'International Shipping',
       'Sales Price', 'Shipping Charges', 'Sales per Unit', 'Quantity',
       'Total Sales', 'Rating', 'Review'"""



#total sale amount according sale per unit
print("total sale amount according sale per unit")
df['perticular product total amount']=df['Sales per Unit'] * df['Sales Price']
print(df['perticular product total amount'])
                                                                    #sale price=100  sale per unit =10 = 1000

#actual price of product
print("actual price of product")
df['actual price']=df['Sales Price'] + df['Shipping Charges']
print(df['actual price'])

#profit margin
print("profit margin")
df['profit_margin']=df['actual price']- df['Sales Price']
print(df['profit_margin'])


#time based analysis

print("time based analysis year month")
df['order year']=df['Order Date'].dt.year
print(df['order year'])


df['order month']=df['Order Date'].dt.month
print(df['order month'])


#sales by region

print("Sales By Region")
sales_by_location=df.groupby('Order Location')['Sales per Unit'].sum().sort_values(ascending=False)
print(sales_by_location)

print("Location Wise Shipping charges")
location_wise_shipping_charge=df.groupby('Order Location')['Shipping Charges'].max().sort_values(ascending=False).head(5)
print(location_wise_shipping_charge)


print("Category Wise Quantity")
category_wise_quantity=df.groupby('Product Category')['Quantity'].sum()
print(category_wise_quantity)


print("Category Wise Avg Rating")
category_wise_rating=df.groupby('Product Category')['Rating'].mean().sort_values(ascending=False)
print(category_wise_rating)


print("Location Wise Top 10 Sale")
location_wise_top_sale=df.groupby('Order Location')['Total Sales'].sum().head(10).sort_values(ascending=False)
print(location_wise_top_sale)


print("Location Wise Quantity Count")
location_wise_quantity_count=df.groupby('Order Location')['Quantity'].count().head(10)
print(location_wise_quantity_count)


print("Month Wise Sale Trend")
month_wise_sales_trend=df.groupby(df['order month'])['Sales per Unit'].sum()
print(month_wise_sales_trend)


id_wise_int_shipping=df.groupby('Order ID')['International Shipping'].count()
print(id_wise_int_shipping)

#visualization

#1)univariate  analysis

numericalcol=['Sales Price', 'Shipping Charges', 'Quantity','Sales per Unit']

for col in numericalcol:
    plt.figure(figsize=(10,6))
    sns.histplot(df[col],kde=True,color="purple")
    plt.title(f"Distribution of {col}")
    plt.show()


categorialcol=['Product Category','Buyer Gender','Order Location']
for col in categorialcol:
    plt.figure(figsize=(10,8))
    value_count=df[col].value_counts()
    plt.bar(value_count.index,value_count.values,color="gray")
    plt.title(f"Distribution of {col}")
    plt.xlabel(col)
    plt.ylabel("count")
    plt.show()


#bivariate analysis

plt.figure(figsize=(10,5))
sns.barplot(x=location_wise_top_sale.index,y=location_wise_top_sale.values,palette="Blues")
plt.title("location wise sale")
plt.xlabel("location")
plt.ylabel("sales")
plt.xticks(rotation=45)
plt.show()



plt.figure(figsize=(10,5))
sns.barplot(x=location_wise_shipping_charge.index,y=location_wise_shipping_charge.values,palette="hls")
plt.title("location wise shipping charge")
plt.xlabel("location")
plt.ylabel("shipping charge")
plt.xticks(rotation=45)
plt.show()



plt.figure(figsize=(10,5))
sns.barplot(x=category_wise_quantity.index,y=category_wise_quantity.values,palette="muted")
plt.title("category_wise_quantity")
plt.xlabel("category")
plt.ylabel("quantity")
plt.xticks(rotation=45)
plt.show()



plt.figure(figsize=(10,8))
sns.barplot(x=location_wise_quantity_count.index,y=location_wise_quantity_count.values,palette="husl")
plt.title("location_wise_quantity")
plt.xlabel("location")
plt.ylabel("quantity")
plt.xticks(rotation=45)
plt.show()





#multivariate analysis

plt.figure(figsize=(10,7))
sns.pairplot(df[numericalcol])
plt.xticks(rotation=45)
plt.show()


plt.figure(figsize=(10,7))
sns.boxplot(x='Product ID',y='Sales per Unit',data=df)
plt.title("id wise sale")
plt.show()


#salestrend as per month
plt.figure(figsize=(10,7))
month_wise_sales_trend.plot()
plt.title('sales trend over the months')
plt.xlabel('order month')
plt.ylabel('total sales')
plt.show()





