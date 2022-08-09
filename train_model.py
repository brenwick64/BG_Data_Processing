# Initial Imports and Dataframe loads
import pickle
import warnings
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd
import tensorflowjs as tfjs
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Surpresses dependency warning outputs
warnings.filterwarnings('ignore')

# Constants
X_FILEPATH = './Processed_Data/x_data.csv'
Y_FILEPATH = './Processed_Data/y_data.csv'
x_data = pd.read_csv(X_FILEPATH)
y_data = pd.read_csv(Y_FILEPATH)
Y_HOUR_GAP = y_data.shape[1]


# __DATA PROCESSING__


def remove_missing_ydata(x_data, y_data):
    # Identify rows with missing data
    row_tracker = []
    for row in y_data.itertuples(name=None):
        if(0.0 in row[1:99]):
            # TODO: Not sure why the extra +2 is needed...
            row_tracker.append(row[0]+2)
    print(f'missing y data: {row_tracker}')
    y_data.iloc[294]

    # Drop rows with corrupted data
    y_data_imputed = y_data.drop(labels=row_tracker, axis=0)
    x_data_imputed = x_data.drop(labels=row_tracker, axis=0)

    return x_data_imputed, y_data_imputed


def scale_to_standard(x_data, y_data):
    standard_scaler = preprocessing.StandardScaler()
    x_data_standard = standard_scaler.fit_transform(
        x_data.iloc[:, 0:x_data.shape[1]])
    y_data_standard = standard_scaler.fit_transform(
        y_data.iloc[:, 0:y_data.shape[1]])

    # Saves standard scaler
    pickle.dump(standard_scaler, open('standard_scaler.pkl', 'wb'))

    return x_data_standard, y_data_standard


# __MODEL CONFIGURATION__


def build_and_train_model(x_train, y_train):
    model = Sequential()
    model.add(Dense(24, input_dim=x.shape[1], activation='relu'))
    model.add(Dense(12, activation='relu'))
    model.add(Dense(Y_HOUR_GAP))
    model.compile(loss='mean_squared_error',
                  optimizer='adam', metrics=['mean_squared_error'])

    # Stops training when there is no improvement in {patience} epochs
    #callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=3)

    #model.fit(x_train, y_train, verbose=2, epochs=100,callbacks=[callback], batch_size=100)

    model.fit(x_train, y_train, verbose=2, epochs=100,
              batch_size=100)

    model.evaluate(x_train, y_train, batch_size=200)

    return model


def export_model(model):
    tfjs.converters.save_keras_model(model, 'TFJSModels')
    json_model = model.to_json()
    with open('Models/model.json', 'w') as json_file:
        json_file.write(json_model)
    model.save_weights('Models/weights.h5')


# __SCRIPT START__

x, y = remove_missing_ydata(x_data, y_data)
x, y = scale_to_standard(x_data, y_data)
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.25, random_state=0)
model = build_and_train_model(x_train, y_train)
test_loss = model.evaluate(x_test, y_test)

export_model(model)
