#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pickle


# In[6]:


data = pd.read_csv(r'FOODYLYTICSDATASET.csv')
data.head()


# In[7]:


data['Menu Rating'].fillna(data['Menu Rating'].mean(), inplace=True)
data['Amount Of Food Cooked'].fillna(data['Amount Of Food Cooked'].mean(), inplace=True)
data['Wastage'].fillna(data['Wastage'].mean(), inplace=True)


# In[8]:


def convert_to_int(word):
    if word == 'Monday':
        return 0
    elif word == 'Tuesday':
        return 1
    elif word == 'Wednesday':
        return 2
    elif word == 'Thursday':
        return 3
    elif word == 'Friday':
        return 4
    elif word == 'Saturday':
        return 5
    elif word == 'Sunday':
        return 6


for i in range(0, data.shape[0]):
    data['Day'][i] = convert_to_int(data['Day'][i])


# In[9]:


predict = "Amount Of Food Cooked"
X = np.array(data.drop([predict], 1))
y = np.array(data[predict])


# In[10]:


x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(
    X, y, test_size=0.3)

linear = linear_model.LinearRegression()

linear.fit(x_train, y_train)
acc = linear.score(x_test, y_test)
print(acc)

#print('Coefficient: \n', linear.coef_)
#print('Intercept: \n', linear.intercept_)


# In[11]:


#

def menu_rating():
    if day1 == 0:
        return 7
    elif day1 == 1:
        return 8.5
    elif day1 == 2:
        return 9.1
    elif day1 == 3:
        return 8.9
    elif day1 == 4:
        return 8.6
    elif day1 == 5:
        return 7
    elif day1 == 6:
        return 7.9


def weekday():
    if(day1 != [5, 6]):
        return 0
    else:
        return 1


def meanwastage():
    mean_wastage = 0
    if(day1 == 0):
        return 153.33333333333
    elif(day1 == 1):
        return 143
    elif(day1 == 2):
        return 107.233
    elif(day1 == 3):
        return 102.233
    elif(day1 == 4):
        return 112.344
    elif(day1 == 5):
        return 349.456
    elif(day1 == 6):
        return 330.233


def convert_to_int(day):
    if day == 'Monday':
        return 0
    elif day == 'Tuesday':
        return 1
    elif day == 'Wednesday':
        return 2
    elif day == 'Thursday':
        return 3
    elif day == 'Friday':
        return 4
    elif day == 'Saturday':
        return 5
    elif day == 'Sunday':
        return 6


# In[12]:


# DAY 0 :MONDAY ; DAY 1:TUESDAY ; DAY 2 :WEDNESDAY ; DAY 3: THURSDAY ; DAY 4:FRIDAY ; DAY 5:SATURDAY ; DAY 6 =SUNDAY
# IF IT IS A WEEKEND THEN TYPE 1, ELSE 0
# CHECK THE AMOUNT THE OF FOOD YOU NEED TO COOK TO MINIMISE YOUR WASTAGE
# By default wastage is 0 since we are trying to predict the ideal amounnt of food to be cooked


# In[13]:


# TESTING
# ------------------
Wastage = 0
# ------------------
day = input('Enter the day of the week: ')
day1 = convert_to_int(day)
weekend = weekday()
mean_wastage = meanwastage()
New_Menu_rating = menu_rating()
pred = linear.predict([[day1, weekend, New_Menu_rating, Wastage]])
print('Menu rating for Today is :', New_Menu_rating)
print('Average wastage on this day: ', mean_wastage, 'Kgs')
print('To avoid this wastage,the predicted amount to be cooked :', pred, 'kgs')
pickle.dump(linear, open('messmodel.pkl', 'wb'))
