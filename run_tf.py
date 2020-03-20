from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf

import sys
training_file = sys.argv[1]
testing_file = sys.argv[2]

def get_data(file_name):
  X = []
  y = []
  f = open(file_name, 'r')
  l = f.readline()
  l = l[:len(l)-1]
  while len(l)>0:
    X.append([int(x) for x in l[:len(l)-1]])
    y.append(int(l[len(l)-1]))
    l = f.readline()
    l = l[:len(l)-1]
  f.close()
  return X, y

X, y = get_data(training_file)

#mnist = tf.keras.datasets.mnist
#(x_train, y_train), (x_test, y_test) = mnist.load_data()
#x_train, x_test = x_train / 255.0, x_test / 255.0


model = tf.keras.models.Sequential([
  tf.keras.layers.Dense(len(X[0]), input_dim=len(X[0]), activation='relu'),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(2, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

#model.fit(x_train, y_train, epochs=5)
model.fit(X, y, epochs=5)

X2, y2 = get_data(testing_file)
model.evaluate(X2,  y2, verbose=2)

