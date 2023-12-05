import queries
import numpy as np
from sklearn.naive_bayes import BernoulliNB
import matplotlib.pyplot as plt

def run_naive_bayes():
  """Use Naive Bayes to predict if a Wikipedia article
  is featured or not.
  """
  # Get the training, validation, and testing data and labels.
  train_data, train_labels, \
  valid_data, valid_labels, \
  test_data, test_labels = queries.load_data()

  priors = [True, False]
  alphas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
  binarizes = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

  results = {
    0.1: [[], []], 
    0.2: [[], []], 
    0.3: [[], []], 
    0.4: [[], []], 
    0.5: [[], []], 
    0.6: [[], []], 
    0.7: [[], []], 
    0.8: [[], []], 
    0.9: [[], []], 
    1: [[], []]
  }

  # Keep the model with highest average accuracy.
  accuracy = 0.0
  final_clf = None
  final_parameters = {"prior": "", "alpha": 0, "binarize": 0}

  # Perform Naive Bayes
  for prior in priors:
    for alpha in alphas:
      for binarize in binarizes:
        clf = BernoulliNB(fit_prior=prior, force_alpha=prior, alpha=alpha, binarize=binarize)
        clf.fit(train_data, train_labels)

        score = clf.score(valid_data, valid_labels)
        results[alpha][0].append(score) if prior else results[alpha][1].append(score)

        if score > accuracy:
          accuracy = score
          final_clf = clf
          final_parameters["prior"] = "True" if prior else "False"
          final_parameters["alpha"] = alpha
          final_parameters["binarize"] = binarize

  # Take the highest average accuracy and use that for testing.
  final_clf.fit(train_data, train_labels)
  print("The final results on the testing set is:", final_clf.score(test_data, test_labels))
  print("The parameters are:")
  print("Prior: %s\nAlpha value: %f\nBinarize value: %f" %(final_parameters["prior"], final_parameters["alpha"], final_parameters["binarize"]))

  # Plot the results
  # results2 = {0.1: [[0.8537180008126778, 0.8468102397399431, 0.8228362454286875, 0.8082080455099553, 0.8057700121901666, 0.8078017066233238, 0.7923608289313288, 0.7830150345388054, 0.7817960178789111, 0.7809833401056481], [0.8504672897196262, 0.8423405119869971, 0.819585534335636, 0.7996749288906948, 0.7952052011377488, 0.7972368955709062, 0.7517269402681837, 0.7391304347826086, 0.7460381958553434, 0.7452255180820805]], 0.2: [[0.8537180008126778, 0.8468102397399431, 0.8228362454286875, 0.8082080455099553, 0.8057700121901666, 0.8078017066233238, 0.7923608289313288, 0.7830150345388054, 0.7817960178789111, 0.7809833401056481], [0.8504672897196262, 0.8423405119869971, 0.819585534335636, 0.7992685900040634, 0.7952052011377488, 0.7972368955709062, 0.7517269402681837, 0.7391304347826086, 0.7460381958553434, 0.7452255180820805]], 0.3: [[0.8537180008126778, 0.8468102397399431, 0.8228362454286875, 0.8082080455099553, 0.8057700121901666, 0.8078017066233238, 0.7923608289313288, 0.7830150345388054, 0.7817960178789111, 0.7809833401056481], [0.8504672897196262, 0.8423405119869971, 0.819585534335636, 0.7992685900040634, 0.7952052011377488, 0.7972368955709062, 0.7517269402681837, 0.7391304347826086, 0.7460381958553434, 0.7452255180820805]], 0.4: [[0.8537180008126778, 0.8468102397399431, 0.822429906542056, 0.8082080455099553, 0.8057700121901666, 0.8078017066233238, 0.7927671678179602, 0.7830150345388054, 0.7817960178789111, 0.7809833401056481], [0.8504672897196262, 0.8419341731003657, 0.818772856562373, 0.7992685900040634, 0.7952052011377488, 0.7972368955709062, 0.7517269402681837, 0.7391304347826086, 0.7460381958553434, 0.7452255180820805]], 0.5: [[0.8533116619260463, 0.8464039008533116, 0.822429906542056, 0.8082080455099553, 0.8057700121901666, 0.8082080455099553, 0.7927671678179602, 0.7830150345388054, 0.7817960178789111, 0.7809833401056481], [0.8504672897196262, 0.8419341731003657, 0.818772856562373, 0.7992685900040634, 0.7952052011377488, 0.7972368955709062, 0.7517269402681837, 0.7391304347826086, 0.7460381958553434, 0.7452255180820805]], 0.6: [[0.8533116619260463, 0.8464039008533116, 0.8220235676554246, 0.8082080455099553, 0.8057700121901666, 0.8082080455099553, 0.7927671678179602, 0.7830150345388054, 0.7817960178789111, 0.7809833401056481], [0.8504672897196262, 0.8415278342137342, 0.8183665176757415, 0.7992685900040634, 0.7952052011377488, 0.7972368955709062, 0.7517269402681837, 0.7391304347826086, 0.7460381958553434, 0.7452255180820805]], 0.7: [[0.8537180008126778, 0.8464039008533116, 0.8220235676554246, 0.8082080455099553, 0.8057700121901666, 0.8082080455099553, 0.7927671678179602, 0.7830150345388054, 0.7817960178789111, 0.7809833401056481], [0.8504672897196262, 0.8415278342137342, 0.8179601787891101, 0.7992685900040634, 0.7952052011377488, 0.7972368955709062, 0.7517269402681837, 0.7391304347826086, 0.7460381958553434, 0.7452255180820805]], 0.8: [[0.8537180008126778, 0.8464039008533116, 0.8220235676554246, 0.8082080455099553, 0.8057700121901666, 0.8082080455099553, 0.7927671678179602, 0.7830150345388054, 0.7817960178789111, 0.7809833401056481], [0.8504672897196262, 0.8415278342137342, 0.8179601787891101, 0.7992685900040634, 0.7952052011377488, 0.7972368955709062, 0.7517269402681837, 0.7391304347826086, 0.7460381958553434, 0.7452255180820805]], 0.9: [[0.8537180008126778, 0.8459975619666802, 0.8220235676554246, 0.8082080455099553, 0.8057700121901666, 0.8086143843965867, 0.7927671678179602, 0.7830150345388054, 0.7817960178789111, 0.7809833401056481], [0.8500609508329947, 0.8415278342137342, 0.8179601787891101, 0.7992685900040634, 0.7952052011377488, 0.7972368955709062, 0.7517269402681837, 0.7395367736692402, 0.7464445347419748, 0.7452255180820805]], 1: [[0.8537180008126778, 0.8459975619666802, 0.8216172287687932, 0.8078017066233238, 0.8057700121901666, 0.8086143843965867, 0.7927671678179602, 0.7830150345388054, 0.7817960178789111, 0.7809833401056481], [0.8500609508329947, 0.8415278342137342, 0.8179601787891101, 0.7992685900040634, 0.7952052011377488, 0.7972368955709062, 0.7517269402681837, 0.7395367736692402, 0.7464445347419748, 0.7456318569687119]]}

  plt.title("Accuracy of Naive Bayes using Alpha Value 0.1")
  plt.xlabel("Binarize Values")
  plt.ylabel("Accuracy (%)")
  plt.plot([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], results[0.1][0])
  plt.plot([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], results[0.1][1])
  plt.legend(["With Prior", "No Prior"])
  plt.figure()

  plt.title("Accuracy of Naive Bayes using Alpha Value 0.2")
  plt.xlabel("Binarize Values")
  plt.ylabel("Accuracy (%)")
  plt.plot([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], results[0.2][0])
  plt.plot([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], results[0.2][1])
  plt.legend(["With Prior", "No Prior"])
  plt.figure()

  plt.title("Accuracy of Naive Bayes using Alpha Value 0.3")
  plt.xlabel("Binarize Values")
  plt.ylabel("Accuracy (%)")
  plt.plot([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], results[0.3][0])
  plt.plot([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], results[0.3][1])
  plt.legend(["With Prior", "No Prior"])
  plt.figure()

  plt.title("Accuracy of Naive Bayes using Alpha Value 0.4")
  plt.xlabel("Binarize Values")
  plt.ylabel("Accuracy (%)")
  plt.plot([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], results[0.4][0])
  plt.plot([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], results[0.4][1])
  plt.legend(["With Prior", "No Prior"])
  plt.figure()

  plt.title("Accuracy of Naive Bayes using Alpha Value 0.5")
  plt.xlabel("Binarize Values")
  plt.ylabel("Accuracy (%)")
  plt.plot([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], results[0.5][0])
  plt.plot([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], results[0.5][1])
  plt.legend(["With Prior", "No Prior"])
  plt.figure()

  plt.title("Accuracy of Naive Bayes using Alpha Value 0.6")
  plt.xlabel("Binarize Values")
  plt.ylabel("Accuracy (%)")
  plt.plot([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], results[0.6][0])
  plt.plot([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], results[0.6][1])
  plt.legend(["With Prior", "No Prior"])
  plt.figure()

  plt.title("Accuracy of Naive Bayes using Alpha Value 0.7")
  plt.xlabel("Binarize Values")
  plt.ylabel("Accuracy (%)")
  plt.plot([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], results[0.7][0])
  plt.plot([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], results[0.7][1])
  plt.legend(["With Prior", "No Prior"])
  plt.figure()

  plt.title("Accuracy of Naive Bayes using Alpha Value 0.8")
  plt.xlabel("Binarize Values")
  plt.ylabel("Accuracy (%)")
  plt.plot([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], results[0.8][0])
  plt.plot([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], results[0.8][1])
  plt.legend(["With Prior", "No Prior"])
  plt.figure()

  plt.title("Accuracy of Naive Bayes using Alpha Value 0.9")
  plt.xlabel("Binarize Values")
  plt.ylabel("Accuracy (%)")
  plt.plot([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], results[0.9][0])
  plt.plot([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], results[0.9][1])
  plt.legend(["With Prior", "No Prior"])
  plt.figure()

  plt.title("Accuracy of Naive Bayes using Alpha Value 1.0")
  plt.xlabel("Binarize Values")
  plt.ylabel("Accuracy (%)")
  plt.plot([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], results[1][0])
  plt.plot([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], results[1][1])
  plt.legend(["With Prior", "No Prior"])
  plt.show()


if __name__ == "__main__":
  run_naive_bayes()