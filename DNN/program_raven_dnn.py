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

## preparing data, this part only need to be run once if the variables are not cleared
#file_path_feature = 'training_ravenstate_rest.txt'
#file_path_label = 'training_img_process_result_rest.txt'
#ravenstate , img_process_result = flr.load_ravenstate_step1(file_path_feature, file_path_label)
#ravenstate , img_process_result ,time_data , time_label = flr.load_ravenstate_step2(ravenstate , img_process_result)
#seed_ravenstate_idx = flr.load_ravenstate_step3(time_data , time_label)

selected_features = np.array([[113,116],[1,4]])
#selected_features = np.array([[1,4]])
selected_labels = np.array([[29,32]])
name_ravenstate , name_CV_result , feature_selection , label_selection , training_data , training_label , data_name , label_name , operation_origin = flr.load_ravenstate_step4(ravenstate , img_process_result , selected_features , selected_labels)
    

# start training
raven_dnn.load_data(data = training_data, label = training_label, 
                    operation_origin = operation_origin, 
                    data_name = data_name, label_name = label_name, 
                    raven_data_signal = 1, 
                    time_data = time_data, time_label = time_label,
                    seed_ravenstate_idx = seed_ravenstate_idx)

raven_dnn.init_system(train_pct = 0.8, vali_pct = 0.15, test_pct = 0.05 , continuous_signal = 1, seperations = 3)


#raven_dnn.info_head(6)
raven_dnn.info_size()

#raven_dnn.info_data_raw()
#raven_dnn.info_data_sets()

raven_dnn.set_operation_pool([1,2,3,4,5,7])

#raven_dnn.dnn_model_init([[1,10],[2,10]])
#raven_dnn.dnn_train(100,100)

raven_dnn.dnn_iter_train(layers_matrix = [[1,1000],[2,900],[3,800],[3,700],[3,600],[3,500],[3,400],[3,300]],
                           learning_rate = 0.000002,
                           regularize_rate = 0,
                           EPOCHS = 6000, 
                           batch_size = 2000,
                           dropping_threshold = 0.05,
                           max_added_features = 10, 
                           max_iteration = 10, 
                           show_plot = True)

##load test data, an unknown traj, this part only need to be run once if the variables are not cleared
#test_ravenstate , test_img_process_result = flr.load_ravenstate_step1('test_ravenstate_seperated.txt', 'test_img_process_result_seperated.txt')
#test_ravenstate , test_img_process_result ,time_data1 , time_label1 = flr.load_ravenstate_step2(test_ravenstate , test_img_process_result)
#name_ravenstate1 , name_CV_result1 , feature_selection1 , label_selection1 , test_feature , test_label , data_name1 , label_name1 , operation_origin1 = flr.load_ravenstate_step4(test_ravenstate , test_img_process_result , selected_features , selected_labels)

raven_dnn.dnn_make_prediction()
raven_dnn.dnn_make_prediction(outside_input_signal = 1 ,data_input = test_feature, output_truth = test_label)
#raven_dnn.dnn_plot_model()
#raven_dnn.dnn_plot_features()
#raven_dnn.dnn_save_model()
#raven_dnn.dnn_error_flag()

label_name = raven_dnn.name_label

