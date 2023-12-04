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
    plotdata = []

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




if __name__ == "__main__":
    train()
