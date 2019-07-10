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
import matplotlib.pyplot as plt

iteration_times = 10
rms_error_x_before_store = np.zeros(iteration_times)
rms_error_x_after_store = np.zeros(iteration_times)
rms_error_y_before_store = np.zeros(iteration_times)
rms_error_y_after_store = np.zeros(iteration_times)
rms_error_z_before_store = np.zeros(iteration_times)
rms_error_z_after_store = np.zeros(iteration_times)

error_std_x_before_store = np.zeros(iteration_times)
error_std_x_after_store = np.zeros(iteration_times)
error_std_y_before_store = np.zeros(iteration_times)
error_std_y_after_store = np.zeros(iteration_times)
error_std_z_before_store = np.zeros(iteration_times)
error_std_z_after_store = np.zeros(iteration_times)


for iteration in range(iteration_times):
    print('[Iteration]:' + str(iteration) + ' |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||')

    # initialize the dnn estimator
    raven_dnn = frd.raven_dnn_estimator()
    
    ## preparing data, this part only need to be run once if the variables are not cleared
    file_path_feature = 'training_ravenstate.txt'
    file_path_label = 'training_img_process_result.txt'
    ravenstate , img_process_result = flr.load_ravenstate_step1(file_path_feature, file_path_label)
    ravenstate , img_process_result ,time_data , time_label = flr.load_ravenstate_step2(ravenstate , img_process_result)
    seed_ravenstate_idx = flr.load_ravenstate_step3(time_data , time_label)
    
#    selected_features = np.array([[1,4], [49,57] ,[81,84] , [113,116]])
    #selected_features = np.array([[1,4]])
    selected_features = np.array([[1,235]])
    selected_labels = np.array([[29,32]])
    name_ravenstate , name_CV_result , feature_selection , label_selection , training_data , training_label , data_name , label_name , operation_origin = flr.load_ravenstate_step4(ravenstate , img_process_result , selected_features , selected_labels)
        
    
    # start training
    raven_dnn.load_data(data = training_data, label = training_label, 
                        operation_origin = operation_origin, 
                        data_name = data_name, label_name = label_name, 
                        raven_data_signal = 1, 
                        time_data = time_data, time_label = time_label,
                        seed_ravenstate_idx = seed_ravenstate_idx)
    
    raven_dnn.init_system(train_pct = 0.9, vali_pct = 0.05, test_pct = 0.05 , continuous_signal = 1, seperations = 4)
    
    
    #raven_dnn.info_head(6)
    raven_dnn.info_size()
    
    #raven_dnn.info_data_raw()
    #raven_dnn.info_data_sets()
    
    #raven_dnn.set_operation_pool([1,2,3,4,5,7])
    raven_dnn.set_operation_pool([1])
    
    #raven_dnn.dnn_model_init([[1,10],[2,10]])
    #raven_dnn.dnn_train(100,100)
    
    raven_dnn.dnn_iter_train(layers_matrix = [[1,600],[2,500],[3,400]],
                               learning_rate = 0.00000001,
                               regularize_rate = 0.000005,
                               EPOCHS = 10000, 
                               batch_size = 1024,
                               dropping_threshold = 0.05,
                               max_added_features = 50, 
                               max_iteration = 0, 
                               show_plot = False,
                               show_operations = False)
    
    
    ##load test data, an unknown traj, this part only need to be run once if the variables are not cleared
    test_ravenstate , test_img_process_result = flr.load_ravenstate_step1('test_ravenstate.txt', 'test_img_process_result.txt')
    test_ravenstate , test_img_process_result ,time_data1 , time_label1 = flr.load_ravenstate_step2(test_ravenstate , test_img_process_result)
    
    name_ravenstate1 , name_CV_result1 , feature_selection1 , label_selection1 , test_feature , test_label , data_name1 , label_name1 , operation_origin1 = flr.load_ravenstate_step4(test_ravenstate , test_img_process_result , selected_features , selected_labels)
    
    dnn_output = raven_dnn.dnn_make_prediction()
    raven_dnn.dnn_make_prediction(outside_input_signal = 1 ,data_input = test_feature, output_truth = test_label)
    
    #raven_dnn.dnn_plot_model()
    #raven_dnn.dnn_plot_features()
    #raven_dnn.dnn_save_model()
    #raven_dnn.dnn_error_flag()
    
    label_name = raven_dnn.name_label
    
    ## Plotting the error before compensation and after compensation
    test_set_seed = raven_dnn.shuffle_seed_test
    
    difference_x_before = img_process_result[29][test_set_seed]
    difference_y_before = img_process_result[30][test_set_seed]
    difference_z_before = img_process_result[31][test_set_seed]
    
    difference_x_after = img_process_result[29][test_set_seed] - dnn_output[0]
    difference_y_after = img_process_result[30][test_set_seed] - dnn_output[1]
    difference_z_after = img_process_result[31][test_set_seed] - dnn_output[2]
    
    rms_error_x_before = np.sqrt(np.average(np.square(difference_x_before)))
    rms_error_x_after = np.sqrt(np.average(np.square(difference_x_after)))
    rms_error_y_before = np.sqrt(np.average(np.square(difference_y_before)))
    rms_error_y_after = np.sqrt(np.average(np.square(difference_y_after)))
    rms_error_z_before = np.sqrt(np.average(np.square(difference_z_before)))
    rms_error_z_after = np.sqrt(np.average(np.square(difference_z_after)))
    
    error_std_x_before = np.std(difference_x_before)
    error_std_x_after = np.std(difference_x_after)
    error_std_y_before = np.std(difference_y_before)
    error_std_y_after = np.std(difference_y_after)
    error_std_z_before = np.std(difference_z_before)
    error_std_z_after = np.std(difference_z_after)
    
    
    print("RMS error before correction (x axis): " + str(rms_error_x_before) + " (mm)")
    print("Residual RMS error after correction (x axis): " + str(rms_error_x_after) + " (mm)")
    print("RMS error before correction (y axis): " + str(rms_error_y_before) + " (mm)")
    print("Residual RMS error after correction (y axis): " + str(rms_error_y_after) + " (mm)")
    print("RMS error before correction (z axis): " + str(rms_error_z_before) + " (mm)")
    print("Residual RMS error after correction (z axis): " + str(rms_error_z_after) + " (mm)")
    
    print("Standard diviation of error before correction (x axis): " +  str(error_std_x_before) + " (mm)")
    print("Standard diviation of error after correction (x axis): " +  str(error_std_x_after) + " (mm)")
    print("Standard diviation of error before correction (y axis): " +  str(error_std_y_before) + " (mm)")
    print("Standard diviation of error after correction (y axis): " +  str(error_std_y_after) + " (mm)")
    print("Standard diviation of error before correction (z axis): " +  str(error_std_z_before) + " (mm)")
    print("Standard diviation of error after correction (z axis): " +  str(error_std_z_after) + " (mm)")
    
    rms_error_x_before_store[iteration] = rms_error_x_before
    rms_error_x_after_store[iteration] = rms_error_x_after
    rms_error_y_before_store[iteration] = rms_error_y_before
    rms_error_y_after_store[iteration] = rms_error_y_after
    rms_error_z_before_store[iteration] = rms_error_z_before
    rms_error_z_after_store[iteration] = rms_error_z_after
    
    error_std_x_before_store[iteration] = error_std_x_before
    error_std_x_after_store[iteration] = error_std_x_after
    error_std_y_before_store[iteration] = error_std_y_before
    error_std_y_after_store[iteration] = error_std_y_after
    error_std_z_before_store[iteration] = error_std_z_before
    error_std_z_after_store[iteration] = error_std_z_after
    

    
#    plt.figure()
#    plt.title('Measurement Error of RAVEN without/with neural network')
#    plt.xlabel('index')
#    plt.ylabel('error of end effector position(x-axis)')
#    plt.plot(difference_x_after,
#             label='Neural Network')
#    plt.plot(difference_x_before,"r--",
#             label = 'Original ravenstate')
#    plt.legend()
#    
#    plt.figure()
#    plt.title('Measurement Error of RAVEN without/with neural network')
#    plt.xlabel('index')
#    plt.ylabel('error of end effector position(y-axis)')
#    plt.plot(difference_y_after,
#             label='Neural Network')
#    plt.plot(difference_y_before,"r--",
#             label = 'Original ravenstate')
#    plt.legend()
#    
#    plt.figure()
#    plt.title('Measurement Error of RAVEN without/with neural network')
#    plt.xlabel('index')
#    plt.ylabel('error of end effector position(z-axis)')
#    plt.plot(difference_z_after,
#             label='Neural Network')
#    plt.plot(difference_z_before,"r--",
#             label = 'Original ravenstate')
#    plt.legend()
#    
#    seed_ravenstate_idx = np.int_(seed_ravenstate_idx)
#    
#    pos_x_ravenstate = ravenstate[1][seed_ravenstate_idx][test_set_seed]
#    pos_y_ravenstate = ravenstate[2][seed_ravenstate_idx][test_set_seed]
#    pos_z_ravenstate = ravenstate[3][seed_ravenstate_idx][test_set_seed]
#    
#    pos_x_CV = img_process_result[1][test_set_seed]
#    pos_y_CV = img_process_result[2][test_set_seed]
#    pos_z_CV = img_process_result[3][test_set_seed]
#    
#    pos_x_compensated = pos_x_ravenstate + dnn_output[0]
#    pos_y_compensated = pos_y_ravenstate + dnn_output[1]
#    pos_z_compensated = pos_z_ravenstate + dnn_output[2]
#    
#    plt.figure()
#    plt.title('End Effector Position (x-axis)')
#    plt.xlabel('index')
#    plt.ylabel('x-axis')
#    plt.plot(pos_x_ravenstate,
#             label='ravenstate')
#    plt.plot(pos_x_compensated,
#             label = 'neural network corrected result')
#    plt.plot(pos_x_CV,"r--",
#             label='Truth')
#    plt.legend()
#    
#    plt.figure()
#    plt.title('y-axis Position')
#    plt.xlabel('index')
#    plt.ylabel('y-axis')
#    plt.plot(pos_y_ravenstate,
#             label='ravenstate')
#    plt.plot(pos_y_compensated,
#             label = 'neural network corrected result')
#    plt.plot(pos_y_CV,"r--",
#             label='Truth')
#    plt.legend()
#    
#    plt.figure()
#    plt.title('z-axis Position')
#    plt.xlabel('index')
#    plt.ylabel('z-axis')
#    plt.plot(pos_z_ravenstate,
#             label='ravenstate')
#    plt.plot(pos_z_compensated,
#             label = 'neural network corrected result')
#    plt.plot(pos_z_CV,"r--",
#             label='Truth')
#    plt.legend()
rms_error_x_before_avg = np.average(rms_error_x_before_store)
rms_error_x_after_avg = np.average(rms_error_x_after_store)
rms_error_y_before_avg = np.average(rms_error_y_before_store)
rms_error_y_after_avg = np.average(rms_error_y_after_store)
rms_error_z_before_avg = np.average(rms_error_z_before_store)
rms_error_z_after_avg = np.average(rms_error_z_after_store)

error_std_x_before_avg = np.average(error_std_x_before_store)
error_std_x_after_avg = np.average(error_std_x_after_store)
error_std_y_before_avg = np.average(error_std_y_before_store)
error_std_y_after_avg = np.average(error_std_y_after_store)
error_std_z_before_avg = np.average(error_std_z_before_store)
error_std_z_after_avg = np.average(error_std_z_after_store)

rms_error_reduce_x_avg = rms_error_x_before_avg - rms_error_x_after_avg
rms_error_reduce_y_avg = rms_error_y_before_avg - rms_error_y_after_avg
rms_error_reduce_z_avg = rms_error_z_before_avg - rms_error_z_after_avg

rms_error_reduce_pct_x_avg = rms_error_reduce_x_avg / rms_error_x_before_avg * 100
rms_error_reduce_pct_y_avg = rms_error_reduce_y_avg / rms_error_y_before_avg * 100
rms_error_reduce_pct_z_avg = rms_error_reduce_z_avg / rms_error_z_before_avg * 100

error_std_reduce_x_avg = error_std_x_before_avg - error_std_x_after_avg
error_std_reduce_y_avg = error_std_y_before_avg - error_std_y_after_avg
error_std_reduce_z_avg = error_std_z_before_avg - error_std_z_after_avg

error_std_reduce_pct_x_avg = error_std_reduce_x_avg / error_std_x_before_avg * 100
error_std_reduce_pct_y_avg = error_std_reduce_y_avg / error_std_y_before_avg * 100
error_std_reduce_pct_z_avg = error_std_reduce_z_avg / error_std_z_before_avg * 100

print('rms error: (before) - (after) || x - y - z:')
print(rms_error_x_before_avg)
print(rms_error_x_after_avg)
print(rms_error_y_before_avg)
print(rms_error_y_after_avg)
print(rms_error_z_before_avg)
print(rms_error_z_after_avg)
print('rms error reduction: value - percentage || x - y - z: ')
print(rms_error_reduce_x_avg)
print(rms_error_reduce_pct_x_avg)
print(rms_error_reduce_y_avg)
print(rms_error_reduce_pct_y_avg)
print(rms_error_reduce_z_avg)
print(rms_error_reduce_pct_z_avg)

print('error std: (before) - (after) || x - y - z:')
print(error_std_x_before_avg)
print(error_std_x_after_avg)
print(error_std_y_before_avg)
print(error_std_y_after_avg)
print(error_std_z_before_avg)
print(error_std_z_after_avg)
print('error std reduction: value - percentage || x - y - z: ')
print(error_std_reduce_x_avg)
print(error_std_reduce_pct_x_avg)
print(error_std_reduce_y_avg)
print(error_std_reduce_pct_y_avg)
print(error_std_reduce_z_avg)
print(error_std_reduce_pct_z_avg)





