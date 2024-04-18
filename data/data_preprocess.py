import numpy as np
import os
import panda as pd
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import StandardScaler
# folder_path = 'data'
##read file in folder
# for filename in os.listdir(folder_path):
#     # Creat file path
#     file_path = os.path.join(folder_path, filename)
#     if os.path.isfile(file_path):
#         # read data
#         df = pd.read_csv(file_path)

df=pd.read_csv('data200.csv')
print(df.head())

#clean data
df.dropna(inplace=True)

#Data Encoding
encoded_df = pd.get_dummies(df, columns=['Label'])

#freaure scaler
scaler = StandardScaler()
numerical_features = ['Accel', 'Gyr']
df[numerical_features] = scaler.fit_transform(df[numerical_features])

#Padding
padded_sequences = pad_sequences(df, padding='post', dtype='int32')# 'int32' may need change
# creat Masking
mask = np.zeros_like(padded_sequences, dtype='bool')
mask[padded_sequences != 0] = True
