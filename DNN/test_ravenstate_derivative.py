# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 13:51:00 2019

@author: 75678
"""

import numpy as np
import matplotlib.pyplot as plt
import func_decay_filter as fdf

ravenstate = np.loadtxt('raven_state_traj1.txt').T
um2mm = 0.001
end_size = 10000
decay_rate = 0.01

for line in ravenstate[1:2]:
    plt.figure()
    plt.xlabel('time')
    plt.ylabel('value')
    plt.title('origin_data')
    plt.plot((ravenstate[0]-ravenstate[0][0])[0:end_size] , um2mm*line[0:end_size],label='origin')
    
#    plt.figure()
#    filtered_dev = np.gradient(fdf.decay_filter_offline(line, decay_rate = 0.005), 0.001 ,edge_order = 2)
#    plt.xlabel('time')
#    plt.ylabel('value')
#    plt.title('first_order_dev')
#    plt.plot((ravenstate[0]-ravenstate[0][0])[0:end_size] , um2mm*filtered_dev[0:end_size])
    
    plt.figure()
    plt.xlabel('time')
    plt.ylabel('value')
    plt.title('unfiltered_first_order_dev')
    plt.plot((ravenstate[0]-ravenstate[0][0])[0:end_size] , np.gradient(line,0.001,edge_order=2)[0:end_size],label='unfiltered first derivative')
    
    plt.figure()
    filtered_dev = fdf.decay_icr_rate_offline(line, dx=0.001 , decay_rate = decay_rate)
    plt.xlabel('time')
    plt.ylabel('value')
    plt.title('first_order_dev')
    plt.plot((ravenstate[0]-ravenstate[0][0])[0:end_size] , um2mm*filtered_dev[0:end_size],label='first derivative')
    

    filtered_dev2 = fdf.decay_icr_rate_offline(filtered_dev, dx=0.001 , decay_rate = decay_rate)
    plt.xlabel('time')
    plt.ylabel('value')
    plt.title('second_order_dev')
    plt.plot((ravenstate[0]-ravenstate[0][0])[0:end_size] , um2mm*filtered_dev2[0:end_size],label='second derivative')
    

    filtered_dev3 = fdf.decay_icr_rate_offline(filtered_dev2, dx=0.001 , decay_rate = decay_rate)
    plt.xlabel('time')
    plt.ylabel('value')
    plt.title('third_order_dev')
    plt.plot((ravenstate[0]-ravenstate[0][0])[0:end_size] , um2mm*filtered_dev3[0:end_size],label='third derivative')
    plt.legend()