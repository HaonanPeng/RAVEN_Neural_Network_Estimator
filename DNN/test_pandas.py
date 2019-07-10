# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 10:00:58 2019

@author: 75678
"""
# Import all libraries needed for the tutorial

# General syntax to import specific functions in a library: 
##from (library) import (specific library function)
from pandas import DataFrame, read_csv

# General syntax to import a library but no functions: 
##import (library) as (give the library a nickname/alias)
import matplotlib.pyplot as plt
import pandas as pd #this is how I usually import pandas
import sys #only needed to determine Python version number
import matplotlib #only needed to determine Matplotlib version number



print('Python version ' + sys.version)
print('Pandas version ' + pd.__version__)
print('Matplotlib version ' + matplotlib.__version__)

# The inital set of baby names and birth rates
names = ['Bob','Jessica','Mary','John','Mel']
births = [968, 155, 77, 578, 973]

BabyDataSet = list(zip(names,births))
BabyDataSet

df = pd.DataFrame(data = BabyDataSet, columns=['Names', 'Births'])
df.describe()

df.to_csv('births1880.csv',index=True, header=True)

Location = r'C:\Users\75678\.spyder-py3\DNN\births1880.csv'
df = pd.read_csv(Location, index=True, header=True)