# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 16:13:56 2019

@author: 75678
"""

import tensorflow as tf
#tf.enable_eager_execution()
import func_raven_dnn2 as frd
import numpy as np
import time

raven_dnn = frd.raven_dnn_estimator()

raven_dnn.test_data_generator()

raven_dnn.dnn_load_model()

raven_dnn.init_system()

raven_dnn.dnn_make_prediction()


raven_dnn.info_size()
raven_dnn.info_data_raw()
raven_dnn.info_data_sets()