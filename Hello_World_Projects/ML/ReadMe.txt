In order to use the predictions model you must include the tensorflow/keras and then
new_model = tf.keras.models.load_model('pathto/FuturePredictionsModel')

Once you have the model loaded into python, to predict is just
predictions = model.predict(dataset)
Then it will return a numpy array of the predictions.
The dataset should look just like the data used to train the model (see FuturePredictions.csv)

