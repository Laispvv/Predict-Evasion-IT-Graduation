import pandas as pd
import numpy as np

def define_target(data:pd.DataFrame):
    conditions = [
    (data['TP_SITUACAO'] == 4) | (data['TP_SITUACAO'] == 5),
    (data['TP_SITUACAO'] == 2) | (data['TP_SITUACAO'] == 6) | (data['TP_SITUACAO'] == 3)
    ]
    # create a list of the values we want to assign for each condition
    values = [1, 0]
    # create a new column and use np.select to assign values to it using our lists as arguments
    return np.select(conditions, values)

def define_deficiencia(row):
    val = 0
    vector = ['IN_DEFICIENCIA', 'IN_DEFICIENCIA_AUDITIVA', 'IN_DEFICIENCIA_FISICA', 'IN_DEFICIENCIA_INTELECTUAL', 'IN_DEFICIENCIA_MULTIPLA',
             'IN_DEFICIENCIA_SURDEZ','IN_DEFICIENCIA_SURDOCEGUEIRA', 'IN_DEFICIENCIA_BAIXA_VISAO', 'IN_DEFICIENCIA_CEGUEIRA','IN_DEFICIENCIA_SUPERDOTACAO',
             'IN_TGD_AUTISMO','IN_TGD_SINDROME_ASPERGER','IN_TGD_SINDROME_RETT','IN_TGD_TRANSTOR_DESINTEGRATIVO']
    for deficiencia in vector:
        if row[deficiencia] == 1:
            val = 1
    return val

def define_financiamento_reembolsavel(row):
    val = 0
    vector = ['IN_FINANCIAMENTO_ESTUDANTIL', 'IN_FIN_REEMB_FIES', 'IN_FIN_REEMB_ESTADUAL', 'IN_FIN_REEMB_MUNICIPAL', 'IN_FIN_REEMB_PROG_IES',
             'IN_FIN_REEMB_ENT_EXTERNA','IN_FIN_REEMB_OUTRA']
    for item in vector:
        if row[item] == 1:
            val = 1
    return val

def define_financiamento_nao_reembolsavel(row):
    val = 0
    vector = ['IN_FIN_NAOREEMB_PROUNI_INTEGR', 'IN_FIN_NAOREEMB_PROUNI_PARCIAL', 'IN_FIN_NAOREEMB_ESTADUAL', 'IN_FIN_NAOREEMB_MUNICIPAL', 
              'IN_FIN_NAOREEMB_PROG_IES', 'IN_FIN_NAOREEMB_ENT_EXTERNA','IN_FIN_NAOREEMB_OUTRA']
    for item in vector:
        if row[item] == 1:
            val = 1
    return val

def define_bolsa_extraclasse(row):
    val = 0
    vector = ['IN_BOLSA_ESTAGIO', 'IN_BOLSA_EXTENSAO', 'IN_BOLSA_MONITORIA', 'IN_BOLSA_PESQUISA']
    for item in vector:
        if row[item] == 1:
            val = 1
    return val

def define_sex(data:pd.DataFrame):
    conditions = [
    (data['TP_SEXO'] == 1),
    (data['TP_SEXO'] == 2)
    ]
    # create a list of the values we want to assign for each condition
    values = [0, 1]
    # create a new column and use np.select to assign values to it using our lists as arguments
    return np.select(conditions, values)