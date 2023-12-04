import queries
import tensorflow as tf
import keras
from keras import layers

def run_neural_network():
  """Use Neural Networks to predict if a Wikipedia article
  is featured or not.
  """
  # Get the training, validation, and testing data and labels.
  train_data, train_labels, \
  valid_data, valid_labels, \
  test_data, test_labels = queries.load_data()

  # Build the model.
  model = keras.Sequential()

  # Add our layers to the model.
  model.add(layers.Dense(14, activation="relu"))
  model.add(layers.Dense(1, activation="sigmoid"))

  adam = keras.optimizers.Adam(learning_rate=0.001) # TODO: Change

  model.compile(loss='binary_crossentropy', optimizer=adam, metrics=["accuracy"])

  model.fit(train_data, train_labels, epochs=100)

  loss_and_metrics = model.evaluate(valid_data, valid_labels)
  print(loss_and_metrics)
  print('Loss = ',loss_and_metrics[0])
  print('Accuracy = ',loss_and_metrics[1])

if __name__ == "__main__":
  run_neural_network()