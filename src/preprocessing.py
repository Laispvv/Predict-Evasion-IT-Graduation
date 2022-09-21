from sklearn.preprocessing import MinMaxScaler
from utils.processing_utils import *
import pandas as pd
import numpy as np

from utils.utils import save_data

def normalize_data(data:pd.DataFrame):
    data['QT_CARGA_HORARIA_TOTAL'] = MinMaxScaler().fit_transform(np.array(data['QT_CARGA_HORARIA_TOTAL']).reshape(-1,1))
    data['QT_CARGA_HORARIA_INTEG'] = MinMaxScaler().fit_transform(np.array(data['QT_CARGA_HORARIA_INTEG']).reshape(-1,1))
    return data

def data_clean(data:pd.DataFrame):
    # removing students that died
    data = data.loc[data['TP_SITUACAO'] != 7]
    # defining the target value
    data['target'] = define_target(data)
    # selecting columns
    data = data[['target',
        'QT_CARGA_HORARIA_INTEG', 'NU_ANO_CENSO', 
        'TP_CATEGORIA_ADMINISTRATIVA', 
        'QT_CARGA_HORARIA_TOTAL',
        'TP_ORGANIZACAO_ACADEMICA', 
        'TP_TURNO', 'TP_COR_RACA', 'NU_IDADE',
        'TP_GRAU_ACADEMICO', 'NU_ANO_INGRESSO'
    ]]
    
    data['ANOS_DESPENDIDOS'] = (data['NU_ANO_CENSO'] - data['NU_ANO_INGRESSO'])
    
    data = normalize_data(data)
    # removing NULL data
    data = data.loc[:, data.isin(['NULL', np.nan]).mean() == 0]
    print(data.NU_ANO_CENSO.unique())
    return data

def data_split(data):
    # selecting 2019 data to test and the rest to train
    df_test_2019 = data.loc[data['NU_ANO_CENSO'] == 2019]
    df_train = data.loc[data['NU_ANO_CENSO'] != 2019]
    print(df_test_2019.shape)
    X_train, X_test = df_train.drop(columns=["target"]), df_test_2019.drop(columns=["target"])
    y_train, y_test = df_train['target'], df_test_2019['target']
    print(X_test.shape)
    return X_train, X_test, y_train, y_test

def preprocessing(data):    
    # data = data_clean(data)
    save_data(data, 'data/clean_data.csv')
    X_train, X_test, y_train, y_test = data_split(data)
    return X_train, X_test, y_train, y_test