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
# tf.config.set_visible_devices([], 'GPU')
# print("asserted")
def plot_loss(history):
  plt.plot(history.history['loss'], label='binary_crossentropy')
  plt.plot(history.history['val_loss'], label='val_loss')
  plt.ylim([0, 10])
  plt.xlabel('Epoch')
  plt.ylabel('Cross Entropy Error')
  plt.legend()
  plt.grid(True)
  plt.savefig('Loss_SPCTLogistic.png')

# checkpoint_path = "C:/Users/Justr/Documents/491/Cp/Anomaly_SPCT.ckpt"
# checkpoint_dir = os.path.dirname(checkpoint_path)

# # Create a callback that saves the model's weights
# cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
#                                                  save_weights_only=True,
#                                                  verbose=1)



fp = ('C:/Users/Justr/Documents/491/Anomaly_SP.csv')
dataset = pd.read_csv(fp)

train_dataset = dataset.sample(frac=0.8, random_state=0)
test_dataset = dataset.drop(train_dataset.index)
# train_dataset = dataset.drop(train_dataset.index)
print(test_dataset)
train_features = train_dataset.copy()
test_features = test_dataset.copy()
print(train_features)
# #remove value label since that is what you are predicting
train_labels = train_features.pop('Anomaly')
test_labels = test_features.pop('Anomaly')
garbage = train_features.pop('Unnamed: 0')
garbage_test = test_features.pop('Unnamed: 0')

normalizer = preprocessing.Normalization()
normalizer.adapt(np.array(train_features))

print("running")
Logistic_Model = keras.Sequential([
    normalizer,
    layers.Dense(256, activation='relu'),
    layers.Dense(256, activation='relu'),
    layers.Dense(256, activation='relu'),
    keras.layers.Dense(3, activation = 'softmax')
])

Logistic_Model.compile(optimizer='rmsprop', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

history = Logistic_Model.fit(
    train_features, train_labels, 
    epochs=100,
    # suppress logging
    verbose=1,
    batch_size=1000,
    # Calculate validation results on 20% of the training data
    validation_split = 0.2)



Logistic_Model.save('Test_Logistic_SP_no_Index')
plot_loss(history)


test_results = {}
test_results['Logistic_Model'] = Logistic_Model.evaluate(
    test_features, test_labels, verbose=1)
print(test_results)
test_predictions = Logistic_Model.predict(test_features).flatten()
