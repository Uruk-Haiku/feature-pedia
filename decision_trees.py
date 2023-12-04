import queries
import numpy as np
import matplotlib.pyplot as plt
import sklearn
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_graphviz
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

def train():
    """
    Train a decision tree model to guess whether an article is featured.
    """

    training_data, training_labels, \
    validation_data, validation_labels, \
    test_data, test_labels = ...  # TODO data loader

    # Evaluation Criteria
    criteria = ["gini", "entropy", "log_loss"]

    # Stores final best result
    best_hypers = [str, int, 0.]  # Store best criterion-max_depth-success_rate triplet

    # Graphing variables
    depths = range(10)
    plotdata = {"gini": [], "entropy": [], "log_loss": []}

    for max_depth in depths:
        for criterion in criteria:
            # Train
            classifier = DecisionTreeClassifier(criterion=criterion, max_depth=max_depth)
            classifier = classifier.fit(training_data, training_labels)

            # Validate
            prediction = classifier.predict(validation_data)
            num_correct = 0
            for k in range(len(prediction)):
                if prediction[k] == validation_labels[k]:
                    num_correct += 1

            success_rate = num_correct / len(prediction)
            plotdata[criterion].append(success_rate)  # Append success rate
            print("Results for criterion: " + criterion + " and maxdepth: " +
                  str(max_depth) + " >>> " + " Success Rate == " +
                  str(success_rate))

            if success_rate > best_hypers[2]:
                best_hypers[0] = criterion
                best_hypers[1] = max_depth
                best_hypers[2] = success_rate

    # Test
    classifier = DecisionTreeClassifier(criterion=best_hypers[0], max_depth=best_hypers[1])
    classifier = classifier.fit(training_data, training_labels)
    prediction = classifier.predict(test_data)

    num_correct = 0
    for k in range(len(prediction)):
        if prediction[k] == validation_labels[k]:
            num_correct += 1

    success_rate = num_correct / len(prediction)

    # Report
    print()
    print("Best Hyperparameters >>> Criteria: " + best_hypers[0] +
          "  Max Depth: " + best_hypers[1] +
          ".  Success Rate: " + success_rate)

    # Graph





if __name__ == "__main__":
    train()
