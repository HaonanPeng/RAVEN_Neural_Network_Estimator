# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 17:15:55 2019

@author: 75678
"""

import numpy as np
import func_name_ravenstate as fnr

# These functions are set because this part of code is very slow, for multiple running, this part needs to be run only once.
# It will provide variables about ravenstate and index seeds

def load_ravenstate_step1():
    ravenstate = np.loadtxt('training_ravenstate.txt').T
    img_process_result = np.loadtxt('training_img_process_result.txt').T
    return ravenstate , img_process_result

def load_ravenstate_step2(ravenstate , img_process_result):
    um2mm = 0.001
    size_ravenstate = np.shape(ravenstate)
    
    T_0_w = np.array([[0,1,0,-63.2],
                      [0,0,1,230.71],
                      [1,0,0,428.65],
                      [0,0,0,1]])

    # transfer ravenstate's position (um) in frame 0 into computer vision system's position (mm) in frame world
    pos = np.ones((4,size_ravenstate[1]))
    pos[0:3,:] = ravenstate[1:4,:]*um2mm
    pos_frameWorld = T_0_w.dot(pos)
    ravenstate[1:4,:] = pos_frameWorld[0:3,:]
    
    pos_d = np.ones((4,size_ravenstate[1]))
    pos_d[0:3,:] = ravenstate[7:10,:]*um2mm
    pos_d_frameWorld = T_0_w.dot(pos_d)
    ravenstate[7:10,:] = pos_d_frameWorld[0:3,:]
    
    time_data = ravenstate[0]
    time_label = img_process_result[0]
    
    return ravenstate , time_data , time_label

def load_ravenstate_step3(time_data , time_label):
    seed_ravenstate_idx = np.zeros(np.size(time_label))
    idx = 0
    for label_time_value in time_label:
        seed_ravenstate_idx[idx] = find_nearest(time_data , label_time_value)
        idx = idx + 1    
    return seed_ravenstate_idx
    

def load_ravenstate_step4(ravenstate , img_process_result , selected_features , selected_labels):
#    feature_selection = fnr.selected_idx_generator([[1,4],[81,89],[113,121]])
#    label_selection = fnr.selected_idx_generator([[29,32]])
    name_ravenstate = fnr.name_ravenstate
    name_CV_result = fnr.name_CV_result

    feature_selection = fnr.selected_idx_generator(selected_features)
    label_selection = fnr.selected_idx_generator(selected_labels)
    
    training_data = ravenstate[feature_selection]
    training_label = img_process_result[label_selection]
    
    data_name = fnr.name_list_generator(name_ravenstate , feature_selection)
    label_name = fnr.name_list_generator(name_CV_result , label_selection)
    
    operation_origin = np.int_(np.ones((feature_selection.size , 2)) * -1)
    
    return name_ravenstate , name_CV_result , feature_selection , label_selection , training_data , training_label , data_name , label_name , operation_origin
    
    
# This is a function to find the nearest value 
def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx



