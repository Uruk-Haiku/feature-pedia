import queries
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

def run_logistic_regression():
  """Use Logistic Regression to predict if a Wikipedia article
  is featured or not.
  """
  # Get the training, validation, and testing data and labels.
  train_data, train_labels, \
  valid_data, valid_labels, \
  test_data, test_labels = queries.load_data()

  # Set all of the different hyperparameters to try.
  solvers = {
    "lbfgs": {"l2": [], "None": []},
    "liblinear": {"l1": [], "l2": []},
    "newton-cg": {"l2": [], "None": []}, 
    "newton-cholesky": {"l2": [], "None": []}, 
    "sag": {"l2": [], "None": []},
    "saga": {"elasticnet": [], "l1": [], "l2": [], "None": []}
  }

  # Keep the model with highest average accuracy.
  accuracy = 0.0
  final_clf = None

  # Perform Logistic Regression.
  for solver in solvers:
    for penalty in solvers[solver]:

      chosen_penalty = None if penalty == "None" else penalty
      l1_ratio = 0.5 if penalty == "elasticnet" else None

      for iteration in range(100):
        clf = LogisticRegression(solver=solver, penalty=chosen_penalty, l1_ratio=l1_ratio, max_iter=iteration)
        clf.fit(train_data, train_labels)

        score = clf.score(valid_data, valid_labels)
        solvers[solver][penalty].append(score)

        if iteration == 99 and score > accuracy:
          accuracy = score
          final_clf = clf

  # Print out the final results.
  print("The accuracy using the max number (100) of iterations is:")
  print("Solver: %s\nPenalty: %s\nAccuracy: %f\n" %("lbfgs", "l2", solvers["lbfgs"]["l2"][-1]))
  print("Solver: %s\nPenalty: %s\nAccuracy: %f\n" %("lbfgs", "None", solvers["lbfgs"]["None"][-1]))

  print("Solver: %s\nPenalty: %s\nAccuracy: %f\n" %("liblinear", "l1", solvers["liblinear"]["l1"][-1]))
  print("Solver: %s\nPenalty: %s\nAccuracy: %f\n" %("liblinear", "l2", solvers["liblinear"]["l2"][-1]))

  print("Solver: %s\nPenalty: %s\nAccuracy: %f\n" %("newton-cg", "l2", solvers["newton-cg"]["l2"][-1]))
  print("Solver: %s\nPenalty: %s\nAccuracy: %f\n" %("newton-cg", "None", solvers["newton-cg"]["None"][-1]))

  print("Solver: %s\nPenalty: %s\nAccuracy: %f\n" %("newton-cholesky", "l2", solvers["newton-cholesky"]["l2"][-1]))
  print("Solver: %s\nPenalty: %s\nAccuracy: %f\n" %("newton-cholesky", "None", solvers["newton-cholesky"]["None"][-1]))

  print("Solver: %s\nPenalty: %s\nAccuracy: %f\n" %("sag", "l2", solvers["sag"]["l2"][-1]))
  print("Solver: %s\nPenalty: %s\nAccuracy: %f\n" %("sag", "None", solvers["sag"]["None"][-1]))

  print("Solver: %s\nPenalty: %s\nAccuracy: %f\n" %("saga", "elasticnet", solvers["saga"]["elasticnet"][-1]))
  print("Solver: %s\nPenalty: %s\nAccuracy: %f\n" %("saga", "l1", solvers["saga"]["l1"][-1]))
  print("Solver: %s\nPenalty: %s\nAccuracy: %f\n" %("saga", "l2", solvers["saga"]["l2"][-1]))
  print("Solver: %s\nPenalty: %s\nAccuracy: %f\n" %("saga", "None", solvers["saga"]["None"][-1]))

  # Take the highest average accuracy and use that for testing.
  final_clf.fit(train_data, train_labels)
  print("Final results on the testing set:", final_clf.score(test_data, test_labels))


  # plot the results
  plt.title("Mean Accuracy Using The lbfgs Solver")
  plt.xlabel("Number of Iterations")
  plt.ylabel("Mean Accuracy")
  plt.plot([x for x in range(100)], solvers["lbfgs"]["l2"])
  plt.plot([x for x in range(100)], solvers["lbfgs"]["None"])
  plt.legend(["l2", "None"])
  plt.figure()

  plt.title("Mean Accuracy Using The liblinear Solver")
  plt.xlabel("Number of Iterations")
  plt.ylabel("Mean Accuracy")
  plt.plot([x for x in range(100)], solvers["liblinear"]["l1"])
  plt.plot([x for x in range(100)], solvers["liblinear"]["l2"])
  plt.legend(["l1", "l2"])
  plt.figure()

  plt.title("Mean Accuracy Using The newton-cg Solver")
  plt.xlabel("Number of Iterations")
  plt.ylabel("Mean Accuracy")
  plt.plot([x for x in range(100)], solvers["newton-cg"]["l2"])
  plt.plot([x for x in range(100)], solvers["newton-cg"]["None"])
  plt.legend(["l2", "None"])
  plt.figure()

  plt.title("Mean Accuracy Using The newton-cholesky Solver")
  plt.xlabel("Number of Iterations")
  plt.ylabel("Mean Accuracy")
  plt.plot([x for x in range(100)], solvers["newton-cholesky"]["l2"])
  plt.plot([x for x in range(100)], solvers["newton-cholesky"]["None"])
  plt.legend(["l2", "None"])
  plt.figure()

  plt.title("Mean Accuracy Using The sag Solver")
  plt.xlabel("Number of Iterations")
  plt.ylabel("Mean Accuracy")
  plt.plot([x for x in range(100)], solvers["sag"]["l2"])
  plt.plot([x for x in range(100)], solvers["sag"]["None"])
  plt.legend(["l2", "None"])
  plt.figure()

  plt.title("Mean Accuracy Using The saga Solver")
  plt.xlabel("Number of Iterations")
  plt.ylabel("Mean Accuracy")
  plt.plot([x for x in range(100)], solvers["saga"]["elasticnet"])
  plt.plot([x for x in range(100)], solvers["saga"]["l1"])
  plt.plot([x for x in range(100)], solvers["saga"]["l2"])
  plt.plot([x for x in range(100)], solvers["saga"]["None"])
  plt.legend(["elasticnet", "l1", "l2", "None"])
  plt.show()


if __name__ == "__main__":
  run_logistic_regression()
