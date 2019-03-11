# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 15:50:06 2019

@author: 75678
"""

import numpy as np

#input_array shape should be (x,)
def decay_filter_offline(input_array, decay_rate = 0.02):
    output_array = np.zeros(input_array.shape)
    output_array[0] = np.sum(input_array[0:10])/10
    for index in range(1,input_array.shape[0]):
        output_array[index] = (1-decay_rate)*output_array[index-1] + decay_rate*input_array[index]
    
    return output_array

def decay_icr_rate_offline_old(input_array, dx, decay_rate = 0.02):
    # First, filter out the noise in the input array
    input_array = decay_filter_offline(input_array , decay_rate = decay_rate)
    
    # Next, calculate the time delay
    time_delay = 1.5 * dx / decay_rate
    idx_delay = int(time_delay / dx)
    
    output_array = np.zeros(input_array.shape)
    output_array[0] = np.sum(np.gradient(input_array[(idx_delay-100) : (idx_delay+100)], dx ,edge_order = 2))/100
#    output_array = np.gradient(input_array, dx ,edge_order = 2)
    for index in range(1,input_array.shape[0]):
        output_array[index] = (1-decay_rate)*output_array[index-1] + decay_rate*(input_array[index]-input_array[index-1])/dx
    
    output_array = decay_filter_offline(output_array , decay_rate = decay_rate)
    
    return output_array

def decay_icr_rate_offline(input_array, dx, decay_rate = 0.02):
    # First, filter out the noise in the input array
    input_array = decay_filter_offline(input_array , decay_rate = decay_rate)
    
    # Next, calculate the time delay
#    time_delay = 0
#    idx_delay = 0
    time_delay = 3 * dx / decay_rate
    idx_delay = int(time_delay / dx)
    
    input_array = input_array[idx_delay:-1]
    
    output_array = np.zeros(input_array.shape)
    output_array[0] = np.sum(np.gradient(input_array[0 : 100], dx ,edge_order = 2))/100
#    output_array = np.gradient(input_array, dx ,edge_order = 2)
    for index in range(1,input_array.shape[0]):
        output_array[index] = (1-decay_rate)*output_array[index-1] + decay_rate*(input_array[index]-input_array[index-1])/dx
    
    output_array = decay_filter_offline(output_array , decay_rate = decay_rate)
    
    return output_array
        