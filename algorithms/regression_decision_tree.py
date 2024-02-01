import csv
import os
import random


# Define a TreeNode class for the decision tree
class TreeNode:
    def __init__(
        self, value=None, split_feature=None, threshold=None, left=None, right=None
    ):
        self.value = value  # The predicted value if it's a leaf node
        self.split_feature = split_feature  # The feature used for splitting
        self.threshold = threshold  # Threshold value for splitting
        self.left = left  # Left subtree
        self.right = right  # Right subtree


# Define the DecisionTreeRegressor class
class DecisionTreeRegressor:
    def __init__(self, max_depth=None):
        self.max_depth = max_depth  # Maximum depth of the tree
        self.root = None  # The root node of the decision tree

    def fit(self, X, y, depth=0):
        if depth == self.max_depth or len(set(y)) == 1:
            # If the tree reaches the maximum depth or all values are the same, create a leaf node
            value = sum(y) / len(y)
            return TreeNode(value=value)

        num_features = len(X[0])
        best_split_feature = None
        best_threshold = None
        best_mse = float("inf")

        for feature in range(num_features):
            values = list(set(X[i][feature] for i in range(len(X))))
            for val in values:
                left_indices = [i for i in range(len(X)) if X[i][feature] <= val]
                right_indices = [i for i in range(len(X)) if X[i][feature] > val]
                left_values = [y[i] for i in left_indices]
                right_values = [y[i] for i in right_indices]

                mse = self.calculate_mse(left_values, right_values)
                if mse < best_mse:
                    best_mse = mse
                    best_split_feature = feature
                    best_threshold = val
                    best_left_indices = left_indices
                    best_right_indices = right_indices

        if best_mse == float("inf"):
            # No suitable split found, create a leaf node
            value = sum(y) / len(y)
            return TreeNode(value=value)

        # Recursively build left and right subtrees
        left_subtree = self.fit(
            [X[i] for i in best_left_indices],
            [y[i] for i in best_left_indices],
            depth + 1,
        )
        right_subtree = self.fit(
            [X[i] for i in best_right_indices],
            [y[i] for i in best_right_indices],
            depth + 1,
        )

        return TreeNode(
            split_feature=best_split_feature,
            threshold=best_threshold,
            left=left_subtree,
            right=right_subtree,
        )

    def calculate_mse(self, left_values, right_values):
        mse_left = sum(
            [(val - sum(left_values) / len(left_values)) ** 2 for val in left_values]
        ) / len(left_values)
        mse_right = sum(
            [(val - sum(right_values) / len(right_values)) ** 2 for val in right_values]
        ) / len(right_values)
        mse = (len(left_values) / (len(left_values) + len(right_values))) * mse_left + (
            len(right_values) / (len(left_values) + len(right_values))
        ) * mse_right
        return mse

    def predict(self, X):
        predictions = []
        for sample in X:
            predictions.append(self.predict_single(sample, self.root))
        return predictions

    def predict_single(self, sample, node):
        if node.value is not None:
            return node.value
        if sample[node.split_feature] <= node.threshold:
            return self.predict_single(sample, node.left)
        else:
            return self.predict_single(sample, node.right)


# Load data from the CSV file in the "data" folder
def load_data_from_csv(file_path):
    X = []
    y = []
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            X.append([float(val) for val in row[:-1]])
            y.append(float(row[-1]))
    return X, y


# Define the main function
def main():
    # Load the regression dataset
    data_folder = "data"
    data_file = "dataset_regression.csv"
    file_path = os.path.join(data_folder, data_file)
    X, y = load_data_from_csv(file_path)

    # Split the data into a training set and a testing set (you can use a more advanced method here)
    random.seed(42)
    random.shuffle(X)
    randomw.seed(42)
    random.shuffle(y)
    split_ratio = 0.8
    split_index = int(len(X) * split_ratio)
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]

    # Create and train the decision tree regressor
    max_depth = 5  # You can change the max_depth as needed
    regressor = DecisionTreeRegressor(max_depth=max_depth)
    regressor.root = regressor.fit(X_train, y_train)

    # Make predictions on the test set
    predictions = regressor.predict(X_test)

    # Calculate Mean Squared Error (MSE)
    mse = sum((p - true_val) ** 2 for p, true_val in zip(predictions, y_test)) / len(
        y_test
    )
    print(f"Mean Squared Error: {mse:.2f}")


if __name__ == "__main__":
    main()
