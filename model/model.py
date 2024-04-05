# Import system
import sys
import os

import keras.optimizers

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['PYTHONHASHSEED'] = '42'

# Import scikit-learn and its dependencies
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import confusion_matrix

# import tensorflow and its dependencies
from keras import models
from keras import layers

# Import data processing library
import pandas as pd
import numpy as np

# Import data visual library
import seaborn as sns
import matplotlib.pyplot as plt
import cv2

# Import training and test data
import data


if __name__ == "__main__":

    # Tuning and playing with model setting
    test_size = 0.2
    vali_size = 0.3
    output_unit = 3
    drop_out_rate = 0.5
    learning_rate = 0.001
    n_epochs = 10
    n_batchs = 32
    prediction_threshold = 0.5

    # Splitting into dataset and validation
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, shuffle=False
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=vali_size, shuffle=False
    )

    # Initializing LSTM model
    model = models.Sequential([
        layers.Input(input=(X_train.shape[1:]), batch_size=n_batchs),
        layers.LSTM(units=128, stateful=True, return_sequences=True),
        layers.LSTM(units=64, stateful=True, return_sequences=True),
        layers.LSTM(units=64, return_sequences=False),
        layers.Dense(units=32, activation='relu'),
        layers.Dropout(drop_out_rate),
        layers.Dense(output_unit, activation='softmax')
    ])

    # Compiling model
    model.compile(optimizer=keras.optimizers.SGD(learning_rate=learning_rate),
                  loss=keras.losses.CategoricalCrossentropy(),
                  metrics=keras.metrics.CategoricalAccuracy())

    # Training model
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=n_epochs,
        batch_size=n_batchs,
        shuffle=False,
        verbose=2
    )

    # Plot training data set through graph
    plt.plot(history.history['accuracy'], label='accuracy')
    plt.plot(history.history['val_accuracy'], label='val_accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.ylim([0, 1])
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')
    plt.show()

    # Evaluate the model
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=2)

    # Predictions for the confusion matrix
    y_pred = model.predict(X_test)

    # Visualize confusion matrix for accuracy
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d')
    plt.xlabel('Predicted labels')
    plt.ylabel('True labels')
    plt.title('Confusion Matrix')
    plt.show()

    # Print accuracy, recall, and precision
    print(f'Accuracy: {accuracy_score(y_test, y_pred)}')
    print(f'Recall: {recall_score(y_test, y_pred)}')
    print(f'Precision: {precision_score(y_test, y_pred)}')

    # Save the model for further evaluation

