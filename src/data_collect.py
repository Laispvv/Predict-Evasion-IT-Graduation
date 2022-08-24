from sklearn.datasets import load_wine
import pandas as pd

def data_reduce(data_location:str):
    df = pd.read_csv(data_location,
                     sep='|', encoding='ISO-8859-1')
    # selecting only IT students
    df = df.loc[(df['CO_CINE_ROTULO'].str)[:2] == ('06')]
    return df

def data_collect():
    dados_2019 = data_reduce('Dataset_Reduzido/TIC/SUP_ALUNO_2019_TIC.csv')
    dados_2018 = data_reduce('Dataset_Reduzido/TIC/SUP_ALUNO_2018_TIC.csv')
    dados_2017 = data_reduce('Dataset_Reduzido/TIC/SUP_ALUNO_2017_TIC.csv')
    dados_2016 = data_reduce('Dataset_Reduzido/TIC/SUP_ALUNO_2016_TIC.csv')
    dados_2015 = data_reduce('Dataset_Reduzido/TIC/SUP_ALUNO_2015_TIC.csv')
    dados_2014 = data_reduce('Dataset_Reduzido/TIC/SUP_ALUNO_2014_TIC.csv')
    dados_2013 = data_reduce('Dataset_Reduzido/TIC/SUP_ALUNO_2013_TIC.csv')
    dados_2012 = data_reduce('Dataset_Reduzido/TIC/SUP_ALUNO_2012_TIC.csv')
    dados_2011 = data_reduce('Dataset_Reduzido/TIC/SUP_ALUNO_2011_TIC.csv')
    dados_2010 = data_reduce('Dataset_Reduzido/TIC/SUP_ALUNO_2010_TIC.csv')
    dados_2009 = data_reduce('Dataset_Reduzido/TIC/SUP_ALUNO_2009_TIC.csv')
    
    bases = [dados_2009, dados_2010, dados_2011, dados_2012, dados_2013, dados_2014, dados_2015, dados_2016, dados_2017, dados_2018, dados_2019]
    dados_2009_2019 = pd.concat(bases)
    
    return dados_2009_2019

    