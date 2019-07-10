# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 18:38:38 2019

@author: 75678
"""
import numpy as np
import pandas as pd
import tensorflow as tf
import math
import sys


def test_data_generator():
    x = np.linspace(0, 100, 1000000)
    y = np.linspace(0, 500, 1000000)
    z = np.linspace(0, 10000, 1000000)
    
    w = np.power(x,2).dot(np.log(y.dot(np.sqrt(z))))
    
    m = np.zeros((4,np.size(x)))
    m[0] = x
    m[1] = y
    m[2] = z
    m[3] = w
    
    np.savetxt ("test_data.txt", m )
    
    operation_origin = np.ones((4,2)) * -1
    
    np.savetxt ("test_operation.txt", operation_origin)
    
    return m , operation_origin

# Feature_generator
# The operation should be a matrix of (n,2)
# Where the first column means the operation is on which line of the data (aka object), (-1 means original), 
# and the second column indicate for operation, possible operations are:
# -1: original, no operation will be done
#  1: derivative
#  2: power
#  3: log()
#  4: flag
def feature_generator_total(data_origin, operation_matrix):
    data_matrix = data_origin
    iter_counter = 0
    
    for operation_pair in operation_matrix:
        
        operation_object = int(operation_pair[0])
        operation_type = int(operation_pair[1])
        
        if operation_type == -1: # Original data, do nothing
            a = 1
            
        elif operation_type == 1: # take derivative
            new_line = np.gradient(data_matrix[operation_object], 0.1 ,edge_order = 2)
            data_matrix = np.append(data_matrix,[new_line], axis=0)
            
        elif operation_type == 2: # power
            origin_object = operation_object
            while operation_matrix[origin_object][1] == operation_matrix[operation_object][1]:
                origin_object = int(operation_matrix[origin_object][0])
            new_line = data_matrix[operation_object] * data_matrix[origin_object]
            data_matrix = np.append(data_matrix,[new_line], axis=0)
            
        elif operation_type == 3: #log
            if data_matrix[operation_object].min() > 0:
                new_line = np.log(data_matrix[operation_object])
            else:
                new_line = np.log(data_matrix[operation_object] + data_matrix[operation_object].min() + 0.000000000001)
            data_matrix = np.append(data_matrix,[new_line], axis=0)
            
        iter_counter = iter_counter + 1
        
    return data_matrix
        
        
    
    
    
            
data_origin, operation_origin = test_data_generator()
operation = np.append(operation_origin,[[1,1]],axis = 0)
operation = np.append(operation,[[2,2]],axis = 0)
operation = np.append(operation,[[3,3]],axis = 0)
operation = np.append(operation,[[4,2]],axis = 0)
data_generated = feature_generator_total(data_origin, operation)