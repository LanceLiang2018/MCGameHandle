from keras.layers import Dense
from keras.models import Sequential, load_model
import numpy as np
import threading


model = Sequential()

model.add(Dense(384, input_dim=384, activation='tanh'))
model.add(Dense(128, activation='tanh'))
model.add(Dense(6, activation='softmax'))

model.compile(loss='binary_crossentropy', optimizer='adam')


# ERROR: 错误！不能多线程使用，确保在同一线程内


def thread():
    x = np.zeros((1, 384))
    y = np.zeros((1, 6))

    res = model.train_on_batch(x=x, y=y)
    print(res)


def thread2():
    model2 = Sequential()

    model2.add(Dense(384, input_dim=384, activation='tanh'))
    model2.add(Dense(128, activation='tanh'))
    model2.add(Dense(6, activation='softmax'))

    model2.compile(loss='binary_crossentropy', optimizer='adam')

    x = np.zeros((1, 384))
    y = np.zeros((1, 6))

    res = model2.train_on_batch(x=x, y=y)
    print(res)


t = threading.Thread(target=thread2)
t.setDaemon(True)
t.start()
t.join()

