import os
import tensorflow as tf
from tensorflow import keras
import pandas as pd
#SCRIPT USED FOR COMPARING MODELS POST TRAINING
fp = ('./FuturePrediction.csv')
dataset = pd.read_csv(fp)
#Same dataset as since random_state is seeded
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

FeederA_model = tf.keras.models.load_model('FeederA_FuturePredictionsModelNoIndex')
Full_model =  tf.keras.models.load_model('FuturePredictionsModel')


print("Feeder A results: ")
print( FeederA_model.evaluate(
    test_features, test_labels, verbose=1))

print("Full Model results: ")
print(Full_model.evaluate(
    test_features, test_labels, verbose=1))