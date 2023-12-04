import queries

def run_naive_bayes():
  """Use Naive Bayes to predict if a Wikipedia article
  is featured or not.
  """
  # Get the training, validation, and testing data and labels.
  train_data, train_labels, \
  valid_data, valid_labels, \
  test_data, test_labels = queries.load_data()

if __name__ == "__main__":
  run_naive_bayes()