import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

#If you want to plot the loss
def plot_loss(history):
  plt.plot(history.history['loss'], label='loss (MAE)')
  plt.plot(history.history['val_loss'], label='val_loss')
  plt.ylim([0, 10])
  plt.xlabel('Epoch')
  plt.ylabel('Error [Future kWh]')
  plt.legend()
  plt.grid(True)
  plt.savefig('Loss_futureNoIndex.png')


tf.config.set_visible_devices([], 'GPU')

#Datapath
fp = ('./Single_Phase_Center_Tapped/Future/Data/Single_Phase_Center_Tap_Future.csv')
dataset = pd.read_csv(fp)

#80% of data should be in the training set the rest should be testing data
train_dataset = dataset.sample(frac=0.8, random_state=0)
test_dataset = dataset.drop(train_dataset.index)

# Get a copy to be modified
train_features = train_dataset.copy()
test_features = test_dataset.copy()

#remove value label since that is what you are predicting
train_labels = train_features.pop('Future Value')
test_labels = test_features.pop('Future Value')
#Remove the index that should not exist
garbage = train_features.pop("Unnamed: 0")
garbage_test = test_features.pop("Unnamed: 0")
# Normalizer layer to improve performance and initial weights
normalizer = preprocessing.Normalization()
normalizer.adapt(np.array(train_features))

# Create the model itself as a sequential with 3 dense (FC) relu layers and 1 output
linear_model = tf.keras.Sequential([
    normalizer,
    layers.Dense(256, activation='relu'),
    layers.Dense(256, activation='relu'),
    layers.Dense(256, activation='relu'),
    layers.Dense(1)
])

#compile with 0.001 lr and MAE to limit impact of outliers
linear_model.compile(
    optimizer=tf.optimizers.Adam(learning_rate=0.001),
    loss='mean_absolute_error')


history = linear_model.fit(
    train_features, train_labels, 
    epochs=200,
    verbose=1,
    # Calculate validation results on 20% of the training data
    validation_split = 0.2,
    batch_size=250)

#Save the model
linear_model.save('SinglePhaseCenterTapFutureNoIndex')
plot_loss(history)

#If you train multiple models you can print multiple results to compare
test_results = {}
test_results['linear_model'] = linear_model.evaluate(
    test_features, test_labels, verbose=0)

test_predictions = linear_model.predict(test_features).flatten()
#Plot expected vs actual
a = plt.axes(aspect='equal')
plt.scatter(test_labels, test_predictions)
plt.xlabel('True Values [Future Value kWh]')
plt.ylabel('Predictions [Future Value kWh]')
lims = [0, 70]
plt.xlim(lims)
plt.ylim(lims)
_ = plt.plot(lims, lims)
plt.savefig('Future PredictionsNoIndex.png')