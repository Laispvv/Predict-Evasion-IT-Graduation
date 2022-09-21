from data_collect import data_collect
from preprocessing import preprocessing
from modeling import modeling
from utils.utils import *
from utils.evaluation_utils import plot_all

import numpy as np
import os
import pandas as pd

if __name__ == "__main__":
    os.chdir("..")
    
    # Data collect
    # data = data_collect()
    # save_data(data, "data/raw_data.csv")
    
    # preprocessing
    # data = pd.read_csv('./data/raw_data.csv', encoding='ISO-8859-1')
    data = pd.read_csv('./data/df_modelagem_2009_2019.csv', encoding='ISO-8859-1')
    
    X_train, X_test, y_train, y_test = preprocessing(data)
    save_data(pd.DataFrame(X_train), "data/X_train.csv")
    save_data(pd.DataFrame(X_test), "data/X_test.csv")
    save_data(pd.Series(y_train), "data/y_train.csv")
    save_data(pd.Series(y_test), "data/y_test.csv")
    print(X_train.shape, X_test.shape)
    print(X_train.NU_ANO_CENSO.unique(), X_test.NU_ANO_CENSO.unique())
    print(np.unique(y_train, return_counts=True))
    print(np.unique(y_test, return_counts=True))
    
    # Modeling
    X_test = pd.read_csv('data/X_test.csv')
    y_test = pd.read_csv('data/y_test.csv')
    model = load_model('models/model.pkl')
    model = modeling(X_train, y_train)
    save_model(model, "models/model.pkl")
    
    # Evaluation
    plot_all(X_test, y_test, model)