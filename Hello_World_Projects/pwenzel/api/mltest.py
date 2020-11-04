import math
import matplotlib
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import seaborn as sns
import time
import tensorflow as tf

from datetime import date
from matplotlib import pyplot as plt
from numpy.random import seed
from pylab import rcParams
from sklearn.metrics import mean_squared_error, precision_score
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.utils import plot_model

#### Input params ##################
#stk_path = "./data/VTI.csv"
test_size = 0.2                # proportion of dataset to be used as test set
cv_size = 0.2                  # proportion of dataset to be used as cross-validation set

N = 3                          # for feature at day t, we use lags from t-1, t-2, ..., t-N as features. 
                               # initial value before tuning
lstm_units=128                  # lstm param. initial value before tuning.
dropout_prob=0.99                 # lstm param. initial value before tuning.
optimizer='nadam'               # lstm param. initial value before tuning.
epochs=50                       # lstm param. initial value before tuning.
batch_size=8                   # lstm param. initial value before tuning.

fontsize = 14
ticklabelsize = 14

def get_mape(y_true, y_pred): 
    """
    Compute mean absolute percentage error (MAPE)
    """
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def get_x_y(data, N, offset):
    """
    Split data into x (features) and y (target)
    """
    x, y = [], []
    for i in range(offset, len(data)):
        x.append(data[i-N:i])
        y.append(data[i])
    x = np.array(x)
    y = np.array(y)
    
    return x, y

def get_x_scaled_y(data, N, offset):
    """
    Split data into x (features) and y (target)
    We scale x to have mean 0 and std dev 1, and return this.
    We do not scale y here.
    Inputs
        data     : pandas series to extract x and y
        N
        offset
    Outputs
        x_scaled : features used to predict y. Scaled such that each element has mean 0 and std dev 1
        y        : target values. Not scaled
        mu_list  : list of the means. Same length as x_scaled and y
        std_list : list of the std devs. Same length as x_scaled and y
    """
    x_scaled, y, mu_list, std_list = [], [], [], []
    for i in range(offset, len(data)):
        mu_list.append(np.mean(data[i-N:i]))
        std_list.append(np.std(data[i-N:i]))
        x_scaled.append((data[i-N:i]-mu_list[i-offset])/std_list[i-offset])
        y.append(data[i])
    x_scaled = np.array(x_scaled)
    y = np.array(y)
    
    return x_scaled, y, mu_list, std_list


def train_pred_eval_model(x_train_scaled, \
                          y_train_scaled, \
                          x_cv_scaled, \
                          y_cv, \
                          mu_cv_list, \
                          std_cv_list, \
                          lstm_units=50, \
                          dropout_prob=0.5, \
                          optimizer='adam', \
                          epochs=1, \
                          batch_size=1):
    '''
    Train model, do prediction, scale back to original range and do evaluation
    Use LSTM here.
    Returns rmse, mape and predicted values
    Inputs
        x_train_scaled  : e.g. x_train_scaled.shape=(451, 9, 1). Here we are using the past 9 values to predict the next value
        y_train_scaled  : e.g. y_train_scaled.shape=(451, 1)
        x_cv_scaled     : use this to do predictions 
        y_cv            : actual value of the predictions
        mu_cv_list      : list of the means. Same length as x_scaled and y
        std_cv_list     : list of the std devs. Same length as x_scaled and y 
        lstm_units      : lstm param
        dropout_prob    : lstm param
        optimizer       : lstm param
        epochs          : lstm param
        batch_size      : lstm param
    Outputs
        rmse            : root mean square error
        mape            : mean absolute percentage error
        est             : predictions
    '''
    # Create the LSTM network
    model = Sequential()
    model.add(LSTM(units=lstm_units, return_sequences=True, input_shape=(x_train_scaled.shape[1],1)))
    model.add(Dropout(dropout_prob)) # Add dropout with a probability of 0.5
    model.add(LSTM(units=lstm_units))
    model.add(Dropout(dropout_prob)) # Add dropout with a probability of 0.5
    model.add(Dense(1))

    # Compile and fit the LSTM network
    model.compile(loss='mean_squared_error', optimizer=optimizer, metrics =['accuracy'])
    model.fit(x_train_scaled, y_train_scaled, epochs=epochs, batch_size=batch_size, verbose=0)
    
    # Do prediction
    est_scaled = model.predict(x_cv_scaled)
    est = (est_scaled * np.array(std_cv_list).reshape(-1,1)) + np.array(mu_cv_list).reshape(-1,1)
    
    # Calculate RMSE and MAPE
#     print("x_cv_scaled = " + str(x_cv_scaled))
#     print("est_scaled = " + str(est_scaled))
#     print("est = " + str(est))
    rmse = math.sqrt(mean_squared_error(y_cv, est))
    mape = get_mape(y_cv, est)
    
    return rmse, mape, est, model

def load_data(stock):
    df = pdr.data.DataReader(stock, 'quandl', '2017-01-01', '2020-01-01', api_key='yMvb5-wqKEZFE5zt9zif')

    # Change all column headings to be lower case, and remove spacing
    df.columns = [str(x).lower() for x in df.columns]

    # Sort by datetime
    df.sort_values(by='Date', inplace=True, ascending=True)
    df.index.name = 'date'
    df.reset_index(inplace=True)

    return df

def split(df):
    num_cv = int(cv_size*len(df))
    num_test = int(test_size*len(df))
    num_train = len(df) - num_cv - num_test


    # Split into train, cv, and test
    train_cv = df[:num_train+num_cv][['date', 'adjclose']]
    test = df[num_train+num_cv:][['date', 'adjclose']]
    scaler_final = StandardScaler()
    train_cv_scaled_final = scaler_final.fit_transform(np.array(train_cv['adjclose']).reshape(-1,1))

    return train_cv_scaled_final, test

def ml_test(id):
    stockPrice = load_data(id+'.US')
    train_scaled, test = split(stockPrice)

    x_train_cv_scaled, y_train_cv_scaled = get_x_y(train_scaled, N, N)

    x_test_scaled, y_test, mu_test_list, std_test_list = get_x_scaled_y(np.asarray(stockPrice['adjclose']).reshape(-1,1), N, len(train_scaled))
    print('\n' + str(x_test_scaled.shape) + '\n' + str(y_test.shape))
    rmse, mape, est, model = train_pred_eval_model(x_train_cv_scaled, \
                                            y_train_cv_scaled, \
                                            x_test_scaled, \
                                            y_test, \
                                            mu_test_list, \
                                            std_test_list, \
                                            lstm_units=lstm_units, \
                                            dropout_prob=dropout_prob, \
                                            optimizer=optimizer, \
                                            epochs=epochs, \
                                            batch_size=batch_size)

    # Plot adjusted close over time, only for test set
    rcParams['figure.figsize'] = 10, 8 # width 10, height 8
    matplotlib.rcParams.update({'font.size': 14})

    est_df = pd.DataFrame({'est': est.reshape(-1), 
                        'date': stockPrice[len(train_scaled):]['date']})

    ax = test.plot(x='date', y='adjclose', style='gx-', grid=True)
    ax = est_df.plot(x='date', y='est', style='rx-', grid=True, ax=ax)
    ax.legend(['test', 'predictions using lstm'], loc='upper right')
    ax.set_xlabel("date")
    ax.set_ylabel("USD")
    plt.savefig('plot.png')




