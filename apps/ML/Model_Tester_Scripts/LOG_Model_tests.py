import os

import tensorflow as tf
from tensorflow import keras
import pandas as pd
fp = ('./dataset.csv')
dataset = pd.read_csv(fp)

train_dataset = dataset.sample(frac=0.8, random_state=0)
test_dataset = dataset.drop(train_dataset.index)

train_features = train_dataset.copy()
test_features = test_dataset.copy()

#remove value label since that is what you are predicting
train_labels = train_features.pop('Anomaly')
test_labels = test_features.pop('Anomaly')
#Remove the index
garbage = train_features.pop('Unnamed: 0')
garbage_test = test_features.pop('Unnamed: 0')

LogitModel = tf.keras.models.load_model('PathToLogitModel')


print("Logit Model results: ")
print( LogitModel.evaluate(
    test_features, test_labels, verbose=1))