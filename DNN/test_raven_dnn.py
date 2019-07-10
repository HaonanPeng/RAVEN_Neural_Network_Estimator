# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 14:11:19 2019

@author: 75678
"""
import tensorflow as tf
tf.enable_eager_execution()
import func_raven_dnn as frd
import numpy as np


raven_dnn = frd.raven_dnn_estimator()

raven_dnn.test_data_generator()

raven_dnn.feature_generator_total()



raven_dnn.set_percent()

raven_dnn.set_shuffle_seed()

raven_dnn.normalize_data()

raven_dnn.load_shuffled_data()

#raven_dnn.load_operation_txt("test_operation2.txt")
#raven_dnn.show_operation()
#raven_dnn.info()


raven_dnn.add_new_feature([[0,1],[3,2]])
#raven_dnn.show_operation()
#raven_dnn.info()
raven_dnn.show_head()



raven_dnn.creat_dnn_model()
