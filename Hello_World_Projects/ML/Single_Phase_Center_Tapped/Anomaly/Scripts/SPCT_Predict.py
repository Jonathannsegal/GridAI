import os

import tensorflow as tf
from tensorflow import keras

new_model = tf.keras.models.load_model('Test_Logistic_SPCT_no_Index')

test_array = [[7.9677,0.665,1.33,1.33,2.256,2.256,1.504,2017,1,1,4,3.317,10.04,0.0]]
new_model.summary()
ret_val = new_model.predict(test_array)

print(ret_val)