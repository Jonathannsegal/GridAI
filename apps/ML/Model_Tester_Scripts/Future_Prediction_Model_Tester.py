import os

import tensorflow as tf
from tensorflow import keras
import pandas as pd
import numpy as np
fp = ('./Dataset.csv')
dataset = pd.read_csv(fp)

train_dataset = dataset.sample(frac=0.8, random_state=0)
test_dataset = dataset.drop(train_dataset.index)

train_features = train_dataset.copy()
test_features = test_dataset.copy()

#remove value label since that is what you are predicting
train_labels = train_features.pop('Future Value')
test_labels = test_features.pop('Future Value')
#Remove the index
garbage = train_features.pop('Unnamed: 0')
garbage_test = test_features.pop('Unnamed: 0')

Full_model =  tf.keras.models.load_model('PathToPredictionModel')

#AE of the dataset
print(np.mean(np.absolute(test_labels - np.mean(test_labels))))
#Model AE
Full_model.evaluate(test_features, test_labels, verbose = 1)
