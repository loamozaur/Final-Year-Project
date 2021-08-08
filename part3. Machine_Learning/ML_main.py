import pandas as pd
from tensorflow import keras
from tensorflow.keras.layers import Dense, Conv1D, Flatten, MaxPool1D
from keras.models import Sequential
from sklearn.model_selection import train_test_split
import seaborn as sns
import matplotlib.pyplot as plt

header_list = [
     "0VOEM1", "0VOEM2", "0VOEM3", "0VOEM4", "0VOEM5", "0VOEM6", "0VOEM7", "0VOEM8", "0VOEM9", "0VOEM10",
     "0VOEM11", "0VOEM12",
     "1VOEM1", "1VOEM2", "1VOEM3", "1VOEM4", "1VOEM5", "1VOEM6", "1VOEM7", "1VOEM8", "1VOEM9", "1VOEM10",
     "1VOEM11", "1VOEM12",
     "2VOEM1", "2VOEM2", "2VOEM3", "2VOEM4", "2VOEM5", "2VOEM6", "2VOEM7", "2VOEM8", "2VOEM9", "2VOEM10",
     "2VOEM11", "2VOEM12",
     "3VOEM1", "3VOEM2", "3VOEM3", "3VOEM4", "3VOEM5", "3VOEM6", "3VOEM7", "3VOEM8", "3VOEM9", "3VOEM10",
     "3VOEM11", "3VOEM12",
     "S0PhaseTime1", "S0PhaseTime2", "S0PhaseTime3", "S0PhaseTime4", "S0PhaseTime5", "S0PhaseTime6",
     "S1PhaseTime1", "S1PhaseTime2", "S1PhaseTime3", "S1PhaseTime4",
     "S2PhaseTime1", "S2PhaseTime2", "S2PhaseTime3", "S2PhaseTime4", "S2PhaseTime5", "S2PhaseTime6",
     "S3PhaseTime1", "S3PhaseTime2", "S3PhaseTime3",
]

df = pd.read_csv("input/out.csv")

data_input = df.loc[:, header_list]
X = data_input

data_output = df.loc[:, ["AD1", "AD2", "AD3"]]
Y = data_output

X_train, X_val_and_test, Y_train, Y_val_and_test = train_test_split(X, Y, test_size=0.2)
X_val, X_test, Y_val, Y_test = train_test_split(X_val_and_test, Y_val_and_test, test_size=0.5)



"""
model = Sequential([
    keras.layers.Input(shape=(72,)),
    keras.layers.Lambda(lambda x: keras.backend.expand_dims(x, axis=-1)),
    Conv1D(filters=16, kernel_size=3),
    Conv1D(filters=16, kernel_size=4),
    Flatten(),
    Dense(144, activation='relu'),
    Dense(256, activation='relu'),
    Dense(44, activation='relu'),
    Dense(102, activation='relu'),
    Dense(16, activation='relu'),
    Dense(88, activation='relu'),
    Dense(14, activation='relu'),
    Dense(4, activation='relu')
])
"""
model = Sequential([
    keras.layers.Input(shape=(67,)),
    keras.layers.Lambda(lambda x: keras.backend.expand_dims(x, axis=-1)),
    Conv1D(filters=32, kernel_size=3),
    MaxPool1D(),
    Conv1D(filters=32, kernel_size=3),
    MaxPool1D(),
    Flatten(),
    Dense(144, activation='relu'),
    Dense(64, activation='relu'),
    Dense(288, activation='relu'),
    Dense(3, activation='relu')
])
    

model.compile(optimizer="Nadam", loss="mse", metrics="mae")

model.summary()

model.fit(X_train, Y_train, batch_size=100, epochs=72, validation_data=(X_val, Y_val))


print("Model performance on new data:")
model.evaluate(X_test, Y_test)[1]

print("Model performance on the whole data:")
model.evaluate(X, Y)[1]


model.save("model")


""" One input model
import pandas as pd
from tensorflow import keras
from tensorflow.keras.layers import Dense, Conv1D, Flatten, MaxPool1D, Dropout
from keras.models import Sequential
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


header_list = [
     "0VOEM1", "0VOEM2", "0VOEM3", "0VOEM4", "0VOEM5", "0VOEM6", "0VOEM7", "0VOEM8", "0VOEM9", "0VOEM10",
     "0VOEM11", "0VOEM12",
     "1VOEM1", "1VOEM2", "1VOEM3", "1VOEM4", "1VOEM5", "1VOEM6", "1VOEM7", "1VOEM8", "1VOEM9", "1VOEM10",
     "1VOEM11", "1VOEM12",
     "2VOEM1", "2VOEM2", "2VOEM3", "2VOEM4", "2VOEM5", "2VOEM6", "2VOEM7", "2VOEM8", "2VOEM9", "2VOEM10",
     "2VOEM11", "2VOEM12",
     "3VOEM1", "3VOEM2", "3VOEM3", "3VOEM4", "3VOEM5", "3VOEM6", "3VOEM7", "3VOEM8", "3VOEM9", "3VOEM10",
     "3VOEM11", "3VOEM12",
     "S0PhaseTime1", "S0PhaseTime2", "S0PhaseTime3", "S0PhaseTime4", "S0PhaseTime5", "S0PhaseTime6",
     "S1PhaseTime1", "S1PhaseTime2", "S1PhaseTime3", "S1PhaseTime4",
     "S2PhaseTime1", "S2PhaseTime2", "S2PhaseTime3", "S2PhaseTime4", "S2PhaseTime5", "S2PhaseTime6",
     "S3PhaseTime1", "S3PhaseTime2", "S3PhaseTime3"
]

df = pd.read_csv("input/IN1ML.csv")

data_input = df.loc[:, header_list]
X = data_input

data_output = df.loc[:, "AD"]
Y = data_output

X_train, X_val_and_test, Y_train, Y_val_and_test = train_test_split(X, Y, test_size=0.2)
X_val, X_test, Y_val, Y_test = train_test_split(X_val_and_test, Y_val_and_test, test_size=0.5)

print(len(X_train))

model = Sequential([
    keras.layers.Input(shape=(67,)),
    keras.layers.Lambda(lambda x: keras.backend.expand_dims(x, axis=-1)),
    Conv1D(filters=16, kernel_size=3),
    Conv1D(filters=16, kernel_size=4),
    Flatten(),
    Dense(144, activation='relu'),
    Dense(256, activation='relu'),
    Dense(16, activation='relu'),
    Dense(1, activation='relu')
])

model.compile(optimizer="Adam", loss="mean_absolute_error", metrics=["mean_squared_error"])

model.summary()

hist = model.fit(X_train, Y_train, batch_size=100, epochs=72, validation_data=(X_val, Y_val))


print("Model performance on new data:")
model.evaluate(X_test, Y_test)[1]

print("Model performance on the whole data:")
model.evaluate(X, Y)[1]

"""
