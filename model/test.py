"""
Testing area for Tuning HYPER-PARAMETER
"""

# Import module
from model import QuartzClassifier
from helper import get_function_sample
from helper import convert_tflite_to_c

# Import scikit-learn
from sklearn.model_selection import train_test_split


X, y = get_function_sample()

# Create test set
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.3, shuffle=False)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, train_size=0.2, shuffle=False)

# Create an instance of the classifier
model = QuartzClassifier()

# Initialize and train the model (assuming X and y are already defined and preprocessed)
model.initialize(input_shape=X_test)  # Replace None with actual input shape
model.train(X_train, y_train, X_val, y_val)

# Evaluate the model
model.evaluate(X_test, y_test)

# Plot training history
model.plot_history()

# Plot confusion matrix
y_pred = model.model.predict(X_test)  # Assuming you have a test set ready
model.plot_confusion_matrix(y_test, y_pred)

# Save the model
model.save_model()
