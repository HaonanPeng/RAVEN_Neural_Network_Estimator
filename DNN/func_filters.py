# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 15:50:06 2019

@author: 75678
"""

import numpy as np
import sys

def moving_average_filter(data, window_size):
    m = int((window_size - 1) / 2)
    odata = data
    # 处理边缘数据，首尾增加m个首尾项
    for i in range(m):
        first_term = np.array([odata[0]])
        last_term = np.array([odata[-1]])
        odata = np.append(first_term,odata)
        odata = np.append(odata,last_term)
        
    filtered_data = np.zeros(np.size(data))
    for idx in range(len(data)):
        filtered_data[idx] = np.sum(odata[(idx):(idx+2*m+1)])/window_size
    
    return filtered_data

def mov_avr_derivative(data, dt ,window_size):
    filtered_data = moving_average_filter(data, window_size)
    derivative = np.gradient(filtered_data, dt, edge_order = 2)
    filtered_derivative = moving_average_filter(derivative, window_size)
    return filtered_derivative



def create_x(size, rank):
    x = []
    for i in range(2 * size + 1):
        m = i - size
        row = [m**j for j in range(rank)]
        x.append(row) 
    x = np.mat(x)
    return x


def sav_gol_filter(data, window_size, rank):
    m = int((window_size - 1) / 2)
    odata = data
    # 处理边缘数据，首尾增加m个首尾项
    for i in range(m):
        first_term = np.array([odata[0]])
        last_term = np.array([odata[-1]])
        odata = np.append(first_term,odata)
        odata = np.append(odata,last_term)
        
#        np.insert(odata,0,odata[0])
#        np.insert(odata,len(odata),odata[len(odata)-1])
    # 创建X矩阵
    x = create_x(m, rank)
    # 计算加权系数矩阵B
    b = (x * (x.T * x).I) * x.T
    a0 = b[m]
    a0 = a0.T
    # 计算平滑修正后的值
    ndata = []
    for i in range(len(data)):
        y = [odata[i + j] for j in range(window_size)]
        y1 = np.mat(y) * a0
        y1 = float(y1)
        ndata.append(y1)
    return np.array(ndata)

def sav_gol_derivative(data, dt ,window_size, rank):
    filtered_data = sav_gol_filter(data, window_size, rank)
    derivative = np.gradient(filtered_data, dt, edge_order = 2)
    return derivative

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
        