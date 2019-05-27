from keras.layers import Dense
from keras.models import Sequential, load_model
import numpy as np


model = Sequential()

model.add(Dense(384, input_dim=384, activation='tanh'))
model.add(Dense(128, activation='tanh'))
model.add(Dense(6, activation='softmax'))

model.compile(loss='binary_crossentropy', optimizer='adam')

x = np.zeros((1, 384))
y = np.zeros((1, 6))

res = model.train_on_batch(x=x, y=y)
print(res)
