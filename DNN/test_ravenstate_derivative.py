# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 13:51:00 2019

@author: 75678
"""

import numpy as np
import matplotlib.pyplot as plt
import func_decay_filter as fdf

ravenstate = np.loadtxt('raven_state_traj1.txt').T

for line in ravenstate[1:4]:
    plt.figure()
    plt.xlabel('time')
    plt.ylabel('value')
    plt.title('origin_data')
    plt.plot(ravenstate[0]-ravenstate[0][0] , line)
    
    plt.figure()
    filtered_dev = np.gradient(fdf.decay_filter_offline(line, decay_rate = 0.02), 0.001 ,edge_order = 2)
    plt.xlabel('time')
    plt.ylabel('value')
    plt.title('first_order_dev')
    plt.plot(ravenstate[0]-ravenstate[0][0] , filtered_dev)