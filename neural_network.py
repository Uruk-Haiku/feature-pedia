import queries
import tensorflow as tf
import keras
from keras import layers
import matplotlib.pyplot as plt

def run_neural_network():
  """Use Neural Networks to predict if a Wikipedia article
  is featured or not.
  """
  # Get the training, validation, and testing data and labels.
  train_data, train_labels, \
  valid_data, valid_labels, \
  test_data, test_labels = queries.load_data()

  # Hyperparameters
  optimizer_names = ["Adam", "RMSprop", "SGD", "Adagrad", "Nadam"]
  optimizers = [
    keras.optimizers.Adam(learning_rate=0.001), # Adam
    keras.optimizers.RMSprop(learning_rate=0.001),  #RMSprop
    keras.optimizers.SGD(learning_rate=0.001),  #SGD
    keras.optimizers.Adagrad(learning_rate=0.001),  #Adagrad
    keras.optimizers.Nadam(learning_rate=0.001),  #Nadam
  ]
  losses = [
    "binary_crossentropy",
    "kl_divergence",
    "poisson"
  ]
  data = [
    [[], [], []], #Adam
    [[], [], []], #RMSprop
    [[], [], []], #SGD
    [[], [], []], #Adagrad
    [[], [], []]  #Nadam
  ]

  # Keep the model with highest average accuracy.
  accuracy = 0.0
  final_clf = None
  final_parameters = {"optimizer": "", "loss": "", "iteration": 0}

  # Build the model.
  model = keras.Sequential()
  model.add(layers.Dense(14, activation="relu"))
  model.add(layers.Dense(1, activation="sigmoid"))

  for i in range(len(optimizers)):
    for j in range(len(losses)):
      model.compile(loss=losses[j], optimizer=optimizers[i], metrics=["accuracy"])

      # 43 epochs because it is 3 times the number of features.
      for iteration in range(1, 43):
        model.fit(train_data, train_labels, epochs=iteration)
        loss_and_metrics = model.evaluate(valid_data, valid_labels)

        score = loss_and_metrics[1]
        data[i][j].append(score)

        # compare the results.
        if score > accuracy:
          final_clf = model
          final_parameters["optimizer"] = optimizer_names[i]
          final_parameters["loss"] = losses[j]
          final_parameters["iteration"] = iteration


  # Take the highest accuracy and use that for testing.
  final_clf.fit(train_data, train_labels, epochs=42)
  print("Final results on the testing set:", final_clf.evaluate(test_data, test_labels)[1])
  print("The parameters are:")
  print("Optimizer: %s\nLoss: %s\nIteration: %d" %(final_parameters["optimizer"], final_parameters["loss"], final_parameters["iteration"]))

  # plot the results
  plt.title("Accuracy of The Adam Optimizer")
  plt.xlabel("Number of Epochs")
  plt.ylabel("Accuracy (%)")
  plt.plot([x for x in range(1, 43)], data[0][0])
  plt.plot([x for x in range(1, 43)], data[0][1])
  plt.plot([x for x in range(1, 43)], data[0][2])
  plt.legend(["Binary Cross Entropy", "KL Divergence", "Poisson"])
  plt.figure()

  plt.title("Accuracy of The RMSprop Optimizer")
  plt.xlabel("Number of Epochs")
  plt.ylabel("Accuracy (%)")
  plt.plot([x for x in range(1, 43)], data[1][0])
  plt.plot([x for x in range(1, 43)], data[1][1])
  plt.plot([x for x in range(1, 43)], data[1][2])
  plt.legend(["Binary Cross Entropy", "KL Divergence", "Poisson"])
  plt.figure()

  plt.title("Accuracy of The SGD Optimizer")
  plt.xlabel("Number of Epochs")
  plt.ylabel("Accuracy (%)")
  plt.plot([x for x in range(1, 43)], data[2][0])
  plt.plot([x for x in range(1, 43)], data[2][1])
  plt.plot([x for x in range(1, 43)], data[2][2])
  plt.legend(["Binary Cross Entropy", "KL Divergence", "Poisson"])
  plt.figure()

  plt.title("Accuracy of The Adagrad Optimizer")
  plt.xlabel("Number of Epochs")
  plt.ylabel("Accuracy (%)")
  plt.plot([x for x in range(1, 43)], data[3][0])
  plt.plot([x for x in range(1, 43)], data[3][1])
  plt.plot([x for x in range(1, 43)], data[3][2])
  plt.legend(["Binary Cross Entropy", "KL Divergence", "Poisson"])
  plt.figure()

  plt.title("Accuracy of The Nadam Optimizer")
  plt.xlabel("Number of Epochs")
  plt.ylabel("Accuracy (%)")
  plt.plot([x for x in range(1, 43)], data[4][0])
  plt.plot([x for x in range(1, 43)], data[4][1])
  plt.plot([x for x in range(1, 43)], data[4][2])
  plt.legend(["Binary Cross Entropy", "KL Divergence", "Poisson"])
  plt.show()


if __name__ == "__main__":
  run_neural_network()
