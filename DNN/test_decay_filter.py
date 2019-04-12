# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 16:33:38 2019

@author: 75678
"""

import numpy as np
import func_decay_filter as fdf
import matplotlib.pyplot as plt

dx = (10/10000)
decay_rate = 0.005

origin_array = np.cos(np.linspace(0,10,10000))
origin_derivative = -np.sin(np.linspace(0,10,10000))
noisy_array = origin_array + 0.05 * np.random.randn(10000)

filtered_array = fdf.decay_filter_offline(noisy_array)
#noisy_derivative = np.gradient(noisy_array, 0.1 ,edge_order = 2)
#filtered_derivative = fdf.decay_filter_offline(noisy_derivative)
filtered_derivative = fdf.decay_icr_rate_offline(filtered_array , dx = (10/10000) , decay_rate = 0.005)

plt.figure()
plt.xlabel('value')
plt.ylabel('index')
plt.plot(np.linspace(0,10,10000) , noisy_array,label='noisy_array')
plt.plot(np.linspace(0,10,10000) , filtered_array,label='filtered_array')
plt.plot(np.linspace(0,10,10000) , origin_array,label='origin_array')

plt.plot(np.linspace(0,10,10000) , filtered_derivative,label='filtered_derivative')
plt.plot(np.linspace(0,10,10000) + 1.1*dx/decay_rate , origin_derivative,label='origin_derivative')
plt.legend()