"""
Testing area for Tuning HYPER-PARAMETER
"""

# Import module
from model import QuartzClassifier
from helper import convert_tflite_to_c

# Import scikit-learn
from sklearn.model_selection import train_test_split

import numpy as np


def generate_sparse_array(size=(2000, 3)):
    """
    Generate a numpy array with 2000 rows and 3 columns, where each row contains only one number 1
    and the other two numbers are zeros, randomly distributed.

    Parameters:
        size (tuple): Size of the array in the format (rows, columns).

    Returns:
        numpy.ndarray: The generated sparse array.
    """
    # Create an array filled with zeros
    array = np.zeros(size)

    # Randomly choose the indices to place the number 1 in each row
    row_indices = np.random.choice(size[0], size=size[0], replace=False)
    col_indices = np.random.choice(size[1], size=size[0])

    # Set the values to 1 at the chosen indices
    array[row_indices, col_indices] = 1

    return array


X = np.random.random((1000, 20, 1))
y = generate_sparse_array((1000, 3))

print(y)


def drop_remain(X,y):
    remain = X.__len__() % 16
    if remain == 0:
        return X,y
    else:
        X = X[:-remain, :, :]
        y = y[:-remain]
        return X,y


# Create test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=False)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, shuffle=False)

print(X_train.shape, X_val.shape, X_test.shape)

X_train, y_train = drop_remain(X_train, y_train)
X_test, y_test = drop_remain(X_test, y_test)
X_val, y_val = drop_remain(X_val, y_val)

# Create an instance of the classifier
model = QuartzClassifier(output_unit=3, n_batchs=16)

# Initialize and train the model (assuming X and y are already defined and preprocessed)

model.initialize(input_shape=X_test.shape[1:])
model.train(X_train, X_val, y_train, y_val)

# Evaluate the model
model.evaluate(X_test, y_test)

# Plot training history
model.plot_history()

# Plot confusion matrix

y_pred = model.model.predict(X_test,batch_size = 16,verbose = 2)  # Assuming you have a test set ready
print(y_pred.shape)
print(X_test.shape)
print(y_test.shape)
model.plot_confusion_matrix(y_test, y_pred)

# Save the model
model.save_model()
