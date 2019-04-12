# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 15:23:43 2019

@author: 75678
"""
import numpy as np
import func_decay_filter as fdf
import matplotlib.pyplot as plt

final_time = 2
raven_hz = 1000
dx = (1/raven_hz)
decay_rate = 0.01
max_idx = final_time * raven_hz
idx = range(0,final_time)
time = np.linspace(0,final_time,max_idx)

origin_array = np.exp(time)
origin_derivative = -np.sin(time)
noisy_array = origin_array + 0.06 * np.random.randn(max_idx)

filtered_array = fdf.decay_filter_offline(noisy_array,decay_rate)
#noisy_derivative = np.gradient(noisy_array, 0.1 ,edge_order = 2)
#filtered_derivative = fdf.decay_filter_offline(noisy_derivative)
filtered_derivative = fdf.decay_icr_rate_offline(filtered_array , dx = dx , decay_rate = decay_rate)
filtered_derivative2 = fdf.decay_icr_rate_offline(filtered_derivative , dx = dx , decay_rate = decay_rate)
filtered_derivative3 = fdf.decay_icr_rate_offline(filtered_derivative2 , dx = dx , decay_rate = decay_rate)
#filtered_derivative3 = fdf.decay_icr_rate_offline(filtered_derivative2 , dx = dx , decay_rate = decay_rate)

plt.figure()
plt.title('Decay_Rate = ' + str(decay_rate))
plt.xlabel('idx')
plt.ylabel('value')
plt.plot( noisy_array,label='noisy_array')
plt.plot( filtered_derivative3,label='filtered_derivative3')
plt.plot( filtered_derivative2,label='filtered_derivative2')
plt.plot( filtered_derivative,label='filtered_derivative')
#plt.plot( noisy_array,label='noisy_array')
#plt.plot( origin_derivative,label='origin_derivative')
#plt.plot( filtered_array,label='filtered_array')
#plt.plot(time , origin_array,label='origin_array')


#plt.plot( filtered_derivative,label='filtered_derivative')
#plt.plot( -filtered_derivative2,label='-filtered_derivative2')
#plt.plot(time , filtered_derivative3,label='filtered_derivative3')
#plt.plot(time , origin_derivative,label='origin_derivative')
plt.legend()