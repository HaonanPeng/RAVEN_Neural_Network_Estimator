# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 20:13:01 2019

@author: 75678
"""
import tensorflow as tf
#tf.enable_eager_execution()
import numpy as np
import time
import func_raven_dnn2 as frd
import func_name_ravenstate as fnr
import func_load_ravenstate as flr

# initialize the dnn estimator
raven_dnn = frd.raven_dnn_estimator()

# preparing data

ravenstate , img_process_result = flr.load_ravenstate_step1()
ravenstate , time_data , time_label = flr.load_ravenstate_step2(ravenstate , img_process_result)
seed_ravenstate_idx = flr.load_ravenstate_step3(time_data , time_label)

#selected_features = np.array([[1,4],[81,89],[113,121]])
selected_features = np.array([[1,4]])
selected_labels = np.array([[29,32]])
name_ravenstate , name_CV_result , feature_selection , label_selection , training_data , training_label , data_name , label_name , operation_origin = flr.load_ravenstate_step4(ravenstate , img_process_result , selected_features , selected_labels)
    

# start training
raven_dnn.load_data(data = training_data, label = training_label, 
                    operation_origin = operation_origin, 
                    data_name = data_name, label_name = label_name, 
                    raven_data_signal = 1, 
                    time_data = time_data, time_label = time_label,
                    seed_ravenstate_idx = seed_ravenstate_idx)
raven_dnn.init_system()


raven_dnn.info_head(6)
raven_dnn.info_size()

raven_dnn.info_data_raw()
raven_dnn.info_data_sets()

raven_dnn.set_operation_pool([1,2,3,4,5,7])

#raven_dnn.dnn_model_init([[1,10],[2,10]])
#raven_dnn.dnn_train(100,100)

raven_dnn.dnn_iter_train(layers_matrix = [[1,300],[2,300], [3,300]],
                           learning_rate = 0.001,
                           regularize_rate = 0.001,
                           EPOCHS = 2000, 
                           batch_size = 2000,
                           dropping_threshold = 0.05,
                           max_added_features = 10, 
                           max_iteration = 20, 
                           show_plot = False)

raven_dnn.dnn_make_prediction()
raven_dnn.dnn_plot_model()
raven_dnn.dnn_plot_features()
raven_dnn.dnn_save_model()
#raven_dnn.dnn_error_flag()

label_name = raven_dnn.name_label

