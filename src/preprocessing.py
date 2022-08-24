from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from utils.processing_utils import *
import pandas as pd
import numpy as np

def normalize_data(data:pd.DataFrame):
    data['QT_CARGA_HORARIA_TOTAL'] = MinMaxScaler().fit_transform(np.array(data['QT_CARGA_HORARIA_TOTAL']).reshape(-1,1))
    data['QT_CARGA_HORARIA_INTEG'] = MinMaxScaler().fit_transform(np.array(data['QT_CARGA_HORARIA_INTEG']).reshape(-1,1))
    return data

def data_clean(data:pd.DataFrame):
    # dropping columns
    data.drop(columns=['CO_IES_DESTINO'], inplace=True)
    # removing students that died
    data = data.loc[data['TP_SITUACAO'] != 7]
    # defining the target value
    data['target'] = define_target(data)
    # cleaning rows
    data['TEM_DEFICIENCIA'] = data.apply(define_deficiencia, axis=1)
    data['RECEBE_BOLSA_EXTRACURRICULAR'] = data.apply(define_bolsa_extraclasse, axis=1)
    data['FINANCIAMENTO_NAO_REEMBOLSAVEL'] = data.apply(define_financiamento_nao_reembolsavel, axis=1)
    data['FINANCIAMENTO_REEMBOLSAVEL'] = data.apply(define_financiamento_reembolsavel, axis=1)
    # dropping columns
    data.drop(columns=['IN_DEFICIENCIA', 'IN_DEFICIENCIA_AUDITIVA', 'IN_DEFICIENCIA_FISICA', 'IN_DEFICIENCIA_INTELECTUAL', 'IN_DEFICIENCIA_MULTIPLA',
             'IN_DEFICIENCIA_SURDEZ','IN_DEFICIENCIA_SURDOCEGUEIRA', 'IN_DEFICIENCIA_BAIXA_VISAO', 'IN_DEFICIENCIA_CEGUEIRA','IN_DEFICIENCIA_SUPERDOTACAO',
             'IN_TGD_AUTISMO','IN_TGD_SINDROME_ASPERGER','IN_TGD_SINDROME_RETT','IN_TGD_TRANSTOR_DESINTEGRATIVO'], inplace=True)
    data.drop(columns=['IN_RESERVA_ETNICO', 'IN_RESERVA_DEFICIENCIA', 'IN_RESERVA_ENSINO_PUBLICO', 'IN_RESERVA_RENDA_FAMILIAR', 'IN_RESERVA_OUTRA',], inplace=True)
    data.drop(columns=['IN_FINANCIAMENTO_ESTUDANTIL', 'IN_FIN_REEMB_FIES', 'IN_FIN_REEMB_ESTADUAL', 'IN_FIN_REEMB_MUNICIPAL', 'IN_FIN_REEMB_PROG_IES','IN_FIN_REEMB_ENT_EXTERNA','IN_FIN_REEMB_OUTRA'], inplace=True)
    data.drop(columns=['IN_FIN_NAOREEMB_PROUNI_INTEGR', 'IN_FIN_NAOREEMB_PROUNI_PARCIAL', 'IN_FIN_NAOREEMB_ESTADUAL', 'IN_FIN_NAOREEMB_MUNICIPAL', 'IN_FIN_NAOREEMB_PROG_IES', 'IN_FIN_NAOREEMB_ENT_EXTERNA','IN_FIN_NAOREEMB_OUTRA'], inplace=True)
    data.drop(columns=['IN_APOIO_ALIMENTACAO', 'IN_APOIO_BOLSA_PERMANENCIA', 'IN_APOIO_BOLSA_TRABALHO', 'IN_APOIO_MATERIAL_DIDATICO', 'IN_APOIO_MORADIA', 'IN_APOIO_TRANSPORTE'], inplace = True)
    data.drop(columns=['IN_COMPLEMENTAR_ESTAGIO','IN_COMPLEMENTAR_EXTENSAO','IN_COMPLEMENTAR_MONITORIA','IN_COMPLEMENTAR_PESQUISA'], inplace=True)      
    data.drop(columns=['IN_BOLSA_ESTAGIO', 'IN_BOLSA_EXTENSAO', 'IN_BOLSA_MONITORIA', 'IN_BOLSA_PESQUISA'], inplace=True)      
    data.drop(columns=['CO_CINE_ROTULO', 'DT_INGRESSO_CURSO', 'CO_CURSO', 'CO_ALUNO_CURSO', 'CO_IES', 'CO_CURSO_POLO', 'IN_INGRESSO_OUTRO_TIPO_SELECAO', 'TP_SITUACAO'], inplace=True)      
    
    data['ANOS_DESPENDIDOS'] = (data['NU_ANO_CENSO'] - data['NU_ANO_INGRESSO'])
    
    data = normalize_data(data)
    # removing NULL data
    df = df.loc[:, df.isin(['NULL', np.nan]).mean() == 0]
    return data

def data_split(data):
    df_test_2019 = data.loc[data['NU_ANO_CENSO'] == 2019].copy()
    df_train = data.loc[data['NU_ANO_CENSO'] != 2019].copy()
    
    X_train, X_test = df_train.drop(columns=["target"]).copy(), df_test_2019.drop(columns=["target"]).copy() 
    y_train, y_test = df_train['target'].copy(), df_test_2019['target'].copy()
    
    return X_train, X_test, y_train, y_test

def preprocessing(data):    
    X_train, X_test, y_train, y_test = data_split(data)
    return X_train, X_test, y_train, y_test