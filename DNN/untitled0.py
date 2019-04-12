# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 13:30:03 2019

@author: 75678
"""

import numpy as np

a = np.array([])
label_file = open("test_label_name.txt" , "r")
contents = label_file.readlines().replace("\n","")
label_name = ['x', 'y', 'z']

c1 = contents[1]
l1 = label_name[1]
if contents[1] == label_name[1]:
    print("1111111111111")