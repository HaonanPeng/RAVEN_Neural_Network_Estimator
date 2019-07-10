# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 16:00:17 2019

@author: 75678
"""
import numpy as np

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
