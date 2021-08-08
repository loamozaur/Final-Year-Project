import tensorflow as tf
from tensorflow import keras
from keras .layers import Flatten, Dense
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, plot_confusion_matrix
import numpy as np

(train_image, train_label), (test_image, test_label) = keras.datasets.mnist.load_data(path="mnist.npz")

print("train size: ", train_image.shape, train_label.shape)
print("test size: ", test_image.shape, test_label.shape)

train_image = train_image / 255
test_image = test_image / 255

plt.figure(figsize=(10, 10))
for i in range(25):
    plt.subplot(5, 5, i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_image[i], cmap=plt.cm.binary)
    plt.xlabel(train_label[i])
plt.show()

model = keras.Sequential([
    Flatten(input_shape=(28, 28)),
    Dense(48, activation='relu'),
    Dense(10, activation='relu')
])
model.summary()

model.compile(optimizer='Adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(train_image, train_label, epochs=10, batch_size=10)
test_loss, test_acc = model.evaluate(test_image, test_label, verbose=1)
print("Test accuracy: ", test_acc)


'''test_predictions = model.predict(test_image)
disp_matrix_test = plot_confusion_matrix(model, test_label, np.argmax(test_predictions, axis=1))'''
