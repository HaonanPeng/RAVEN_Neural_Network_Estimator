# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 20:13:01 2019

@author: 75678
"""
import tensorflow as tf
#tf.enable_eager_execution()
import func_raven_dnn2 as frd
import numpy as np
import time

raven_dnn = frd.raven_dnn_estimator()

raven_dnn.test_data_generator()
raven_dnn.init_system()


raven_dnn.info_head(6)
raven_dnn.info_size()

raven_dnn.info_data_raw()
raven_dnn.info_data_sets()

raven_dnn.set_operation_pool([1,2,3,4,5,6,7])

#raven_dnn.dnn_model_init([[1,10],[2,10]])
#raven_dnn.dnn_train(100,100)

raven_dnn.dnn_iter_train(layers_matrix = [[1,50],[2,40], [3,30]],
                           learning_rate = 0.001,
                           regularize_rate = 0.01,
                           EPOCHS = 500, 
                           batch_size = 600,
                           dropping_threshold = 0.05,
                           max_added_features = 10, 
                           max_iteration = 10, 
                           show_plot = False)

raven_dnn.dnn_make_prediction()
raven_dnn.dnn_plot_model()
raven_dnn.dnn_plot_features()
raven_dnn.dnn_save_model()
#raven_dnn.dnn_error_flag()

label_name = raven_dnn.name_label

