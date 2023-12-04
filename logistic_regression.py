import csv
import queries
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
import time

def run_logistic_regression():
  """Use Logistic Regression to predict if a Wikipedia article
  is featured or not.
  """
  # Get the training, validation, and testing data and labels.
  train_data, train_labels, \
  valid_data, valid_labels, \
  test_data, test_labels = queries.load_data()

  # Set all of the different hyperparameters to try.
  solvers = {"lbfgs": [], "liblinear": [], "newton-cg": [], "newton-cholesky": [], "sag": [], "saga": []}

  # Perform Logistic Regression.
  clf = LogisticRegression(max_iter=4500).fit(train_data, train_labels)
  print(clf.score(valid_data, valid_labels))

  # iterations = 230
  # score = []

  # for i in range(0, 100):
  #   start_time = time.time()
  #   clf = LogisticRegression(max_iter=i).fit(train_data, train_labels)
  #   end_time = time.time()
  #   score.append(clf.score(valid_data, valid_labels))
  #   print(end_time - start_time)

  # for val in score:
  #   print(val)

if __name__ == "__main__":
  run_logistic_regression()