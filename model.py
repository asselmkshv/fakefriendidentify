import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import Accuracy
from jupyterthemes import jtplot
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

jtplot.style(theme = 'monokai', context = 'notebook', ticks = True, grid = False)

instagram_df_test = pd.read_csv('test.csv')
instagram_df_train = pd.read_csv('train.csv')

x_train = instagram_df_train.drop(columns = ['fake'])
x_test = instagram_df_test.drop(columns = ['fake'])

y_train = instagram_df_train['fake']
y_test = instagram_df_test['fake']

scaler_x = StandardScaler()
X_train = scaler_x.fit_transform(x_train)
X_test = scaler_x.transform(x_test)

Y_train = tf.keras.utils.to_categorical(y_train, num_classes=2)
Y_test = tf.keras.utils.to_categorical(y_test, num_classes=2)

#Building the main model***

model = Sequential()
model.add(Dense(50, input_dim = 11, activation = "relu")) #Initial Layer
model.add(Dropout(0.3))
model.add(Dense(150, activation = "relu"))
model.add(Dropout(0.3))
model.add(Dense(25, activation = "relu"))
model.add(Dropout(0.3))
model.add(Dense(2, activation = "softmax")) #output layer

model.summary()

model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
epochs_hist = model.fit(X_train, Y_train, epochs = 20, verbose = 1, validation_split = 0.1)


# 1.0 = 0  not fake
# 0.1 = 1  fake


def checkAccount(object):
    df = pd.DataFrame(object)
    data = scaler_x.transform(df)
    predicted = model.predict(data)
    if round(predicted[0][0]) == 0:
        if round(predicted[0][1]) == 1:
            return 1
    elif round(predicted[0][1]) == 0:
        if round(predicted[0][0]) == 1:
            return 0
    else:
        return -1
