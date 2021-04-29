import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

#If you want to plot the loss per epoch
def plot_loss(history):
  plt.plot(history.history['loss'], label='loss (MAE)')
  plt.plot(history.history['val_loss'], label='val_loss')
  plt.ylim([0, 10])
  plt.xlabel('Epoch')
  plt.ylabel('Error [Future kWh]')
  plt.legend()
  plt.grid(True)
  plt.savefig('Loss_SinglePhase_SecondaryNoIndex.png')


fp = ('../Data/SinglePhase_Secondary.csv')
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
#Remove index
garbage = train_features.pop('Unnamed: 0')
garbage_test = test_features.pop('Unnamed: 0')

# Normalization layer to improve performance and initial weights
normalizer = preprocessing.Normalization()
normalizer.adapt(np.array(train_features))

# Create the model itself as a sequential with 3 dense (FC) relu layers and 1 final output
linear_model = tf.keras.Sequential([
    normalizer,
    layers.Dense(256, activation='relu'),
    layers.Dense(256, activation='relu'),
    layers.Dense(256, activation='relu'),
    layers.Dense(1)
])

#Compile model using MAE to limit outliers and a learning rate of 0.001
linear_model.compile(
    optimizer=tf.optimizers.Adam(learning_rate=0.001),
    loss='mean_absolute_error')

#Train the model
history = linear_model.fit(
    train_features, train_labels, 
    epochs=200,
    verbose=1,
    # Calculate validation results on 20% of the training data
    validation_split = 0.2)

#Save it
linear_model.save('SinglePhaseSecondaryModelNoIndex')
plot_loss(history)


#If you train multiple models you can print multiple results to compare
test_results = {}
test_results['linear_model'] = linear_model.evaluate(
    test_features, test_labels, verbose=0)

test_predictions = linear_model.predict(test_features).flatten()

a = plt.axes(aspect='equal')
plt.scatter(test_labels, test_predictions)
plt.xlabel('True Values [Future Value kWh]')
plt.ylabel('Predictions [Future Value kWh]')
lims = [0, 70]
plt.xlim(lims)
plt.ylim(lims)
_ = plt.plot(lims, lims)
plt.savefig('SinglePhase_SecondaryNoIndex.png')