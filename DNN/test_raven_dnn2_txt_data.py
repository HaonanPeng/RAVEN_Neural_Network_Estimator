# -*- coding: utf-8 -*-


import tensorflow as tf
#tf.enable_eager_execution()
import func_raven_dnn2 as frd
import numpy as np
import time

raven_dnn = frd.raven_dnn_estimator()

raven_dnn.load_data(data = None, 
                        label = None, 
                        operation_origin = None, 
                        data_name = ["w"], 
                        label_name = ["x","y","z"])

#raven_dnn.load_txt_data(data = None, 
#                        label = None, 
#                        operation_origin = (-1*np.ones(6,2)), 
#                        data_name = ["Encoder1","Encoder2","Encoder3","Encoder4","Encoder5","Encoder6"], 
#                        label_name = ["x","y","z","R_angle","P_angle","Y_angle"])


raven_dnn.init_system()


raven_dnn.info_head(6)
raven_dnn.info_size()

raven_dnn.info_data_raw()
raven_dnn.info_data_sets()

raven_dnn.set_operation_pool([1,2,3,6,7])


raven_dnn.dnn_iter_train(layers_matrix = [[1,50],[2,40], [3,30]],
                           learning_rate = 0.001,
                           regularize_rate = 0.01,
                           EPOCHS = 500, 
                           batch_size = 600,
                           dropping_threshold = 0.05,
                           max_added_features = 10, 
                           max_iteration = 0, 
                           show_plot = False)


raven_dnn.dnn_make_prediction()
raven_dnn.dnn_plot_features()
#raven_dnn.dnn_error_flag()











#raven_dnn.check_gpu()

#tic = time.time()
#raven_dnn.creat_dnn_model()
#print("DNN time used: " + str(time.time() - tic))