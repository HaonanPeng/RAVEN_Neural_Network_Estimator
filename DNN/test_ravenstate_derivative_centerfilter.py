# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 16:19:12 2019

@author: 75678
"""
import numpy as np
import matplotlib.pyplot as plt
import func_sav_gol_filter as fsf
import func_filters as ff

#ravenstate = np.loadtxt('raven_state_traj1.txt').T
um2mm = 0.001
end_size = 10000
window_size = 501
rank = 5

for line in ravenstate[1:2]:
    plt.figure()
    plt.xlabel('time')
    plt.ylabel('value')
    plt.title('origin_data')
    plt.plot((ravenstate[0]-ravenstate[0][0])[0:end_size] , um2mm*line[0:end_size],label='origin')
    plt.plot((ravenstate[0]-ravenstate[0][0])[0:end_size] , ff.moving_average_filter(um2mm*line[0:end_size],window_size),label='origin')
    plt.legend()
#    plt.figure()
#    filtered_dev = np.gradient(fdf.decay_filter_offline(line, decay_rate = 0.005), 0.001 ,edge_order = 2)
#    plt.xlabel('time')
#    plt.ylabel('value')
#    plt.title('first_order_dev')
#    plt.plot((ravenstate[0]-ravenstate[0][0])[0:end_size] , um2mm*filtered_dev[0:end_size])
    
#    plt.figure()
#    plt.xlabel('time')
#    plt.ylabel('value')
#    plt.title('unfiltered_first_order_dev')
#    plt.plot((ravenstate[0]-ravenstate[0][0])[0:end_size] , np.gradient(line,0.001,edge_order=2)[0:end_size],label='unfiltered first derivative')
    
    plt.figure()
    filtered_dev = ff.mov_avr_derivative(line, 0.001 ,window_size )
    plt.xlabel('time')
    plt.ylabel('value')
    plt.title('first_order_dev')
    plt.plot((ravenstate[0]-ravenstate[0][0])[0:end_size] , um2mm*filtered_dev[0:end_size],label='first derivative')
    

    filtered_dev2 = ff.mov_avr_derivative(filtered_dev, 0.001 ,window_size )
    plt.xlabel('time')
    plt.ylabel('value')
    plt.title('second_order_dev')
    plt.plot((ravenstate[0]-ravenstate[0][0])[0:end_size] , um2mm*filtered_dev2[0:end_size],label='second derivative')
    
    filtered_dev3 = ff.mov_avr_derivative(filtered_dev2, 0.001 ,window_size )
    plt.xlabel('time')
    plt.ylabel('value')
    plt.title('third_order_dev')
    plt.plot((ravenstate[0]-ravenstate[0][0])[0:end_size] , um2mm*filtered_dev3[0:end_size],label='third derivative')
    plt.legend()