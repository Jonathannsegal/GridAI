# Authors: Justin Merkel
# Created: TODO
# Updated: 5/3/2021
# Copyrighted 2021 sdmay21-23@iastate.edu
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import sys
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

print(tf.config.list_physical_devices('GPU'))
# Hide GPU from visible devices
tf.config.set_visible_devices([], 'GPU')

#If you want to plot the loss per epoch
def plot_loss(history):
  plt.plot(history.history['loss'], label='sparse_categorical_crossentropy')
  plt.plot(history.history['val_loss'], label='val_loss')
  plt.ylim([0, 10])
  plt.xlabel('Epoch')
  plt.ylabel('Cross Entropy Error')
  plt.legend()
  plt.grid(True)
  plt.savefig('Loss_SPLogistic.png')

#Filepath of the anomaly data
fp = ('../Data/Anomaly_SP.csv')
dataset = pd.read_csv(fp)

#80% of data should be in the training set the rest should be testing data
train_dataset = dataset.sample(frac=0.8, random_state=0)
test_dataset = dataset.drop(train_dataset.index)

# Get a copy to be modified
train_features = train_dataset.copy()
test_features = test_dataset.copy()

# remove value label since that is what you are predicting
train_labels = train_features.pop('Anomaly')
test_labels = test_features.pop('Anomaly')
#Remove the index that should not exist
garbage = train_features.pop('Unnamed: 0')
garbage_test = test_features.pop('Unnamed: 0')

# Normalization layer to improve performance and initial weights
normalizer = preprocessing.Normalization()
normalizer.adapt(np.array(train_features))

# Create the model itself as a sequential with 3 dense (FC) relu layers and a softmax final layer
Logistic_Model = keras.Sequential([
    normalizer,
    layers.Dense(256, activation='relu'),
    layers.Dense(256, activation='relu'),
    layers.Dense(256, activation='relu'),
    keras.layers.Dense(3, activation = 'softmax')
])

# Compile the model with the cross entropy loss and rmsprop decaying learning rate optimizer
Logistic_Model.compile(optimizer='rmsprop', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

#Train the model
history = Logistic_Model.fit(
    train_features, train_labels, 
    epochs=100,
    verbose=1,
    batch_size=1000,
    # Calculate validation results on 20% of the training data
    validation_split = 0.2)


#Save the trained ml model to be used later
Logistic_Model.save('Test_Logistic_SP_no_Index')


#If you train multiple models you can print multiple results to compare
test_results = {}
test_results['Logistic_Model'] = Logistic_Model.evaluate(
    test_features, test_labels, verbose=1)
print(test_results)
plot_loss(history)
test_predictions = Logistic_Model.predict(test_features).flatten()
