from io import StringIO
from unittest import result
import streamlit as st
import requests
import json
import pandas as pd

st.set_page_config(
     page_title="Dropout Monitor",
     page_icon="🎓",
     layout="wide",
)

MODEL_URL = f'http://localhost:8000/predict'
replace_map = {
    'Resultado':{
        0: '✅ Não evadido',
        1: '❌ Evadido'
    }
}

def predict_results(url, value):
    result = requests.post(f"{url}", json=value)
    return json.loads(result.text)
    # st.write("o resultado é:", json.loads(result.text)['prediction'][0])

def mostrar_resultado_previsoes(dataframe):
    st.markdown('### Resultado das previsões 🔍')
    print(dataframe.to_json())
    result = predict_results(MODEL_URL, dataframe.to_json())
    # st.write(result)
    
    proba_evadir, proba_nao_evadir  = [], []
    for item in result['prediction_proba']:
        proba_nao_evadir.append(f'{round(item[0]*100, 2)}%')
        proba_evadir.append(f'{round(item[1]*100, 2)}%')
        
    result_df = pd.DataFrame({'Resultado':result['prediction'], 
                                'Probabilidade de evadir':proba_evadir,
                                'Probabilidade de não evadir': proba_nao_evadir})
    result_df.replace(replace_map, inplace=True)
    st.table(result_df)

def select_categoria_administrativa(TP_CATEGORIA_ADMINISTRATIVA):
    if TP_CATEGORIA_ADMINISTRATIVA == 'Pública Federal':
        return 1
    elif TP_CATEGORIA_ADMINISTRATIVA == 'Pública Estadual':
        return 2
    elif TP_CATEGORIA_ADMINISTRATIVA == 'Pública Municipal':
        return 3
    elif TP_CATEGORIA_ADMINISTRATIVA == 'Privada com fins lucrativos':
        return 4
    elif TP_CATEGORIA_ADMINISTRATIVA == 'Privada sem fins lucrativos':
        return 5
    else:
        return 7
    
def select_organizacao_academica(TP_ORGANIZACAO_ACADEMICA):
    if TP_ORGANIZACAO_ACADEMICA == 'Universidade':
        return 1
    elif TP_ORGANIZACAO_ACADEMICA == 'Centro Universitário':
        return 2
    elif TP_ORGANIZACAO_ACADEMICA == 'Faculdade':
        return 3
    elif TP_ORGANIZACAO_ACADEMICA == 'Instituto Federal de Educação, Ciência e Tecnologia':
        return 4
    else:
        return 5
    
def select_sim_nao(select):
    if select == 'Sim':
        return 1
    else:
        return 0

def select_semestre_entrada(select):
    if select == '1° semestre':
        return 1
    else:
        return 2

def select_escola(select):
    if select == 'Pública':
        return 1
    elif select == 'Privada':
        return 2
    else:
        return 9

def select_turno(select):
    print(select)
    if select == 'Matutino':
        return 1
    elif select == 'Vespertino':
        return 2
    elif select == 'Noturno':
        return 3
    elif select == 'Integral':
        return 4
    else:
        return 0
    
def select_cor_raca(cor_raca):
    print(cor_raca)
    if cor_raca == 'Não declarada':
        return 0
    elif cor_raca == 'Branca':
        return 1
    elif cor_raca == 'Preta':
        return 2
    elif cor_raca == 'Parda':
        return 3
    elif cor_raca == 'Amarela':
        return 4
    elif cor_raca == 'Indígena':
        return 5
    else:
        return 9
    
def select_grau_academico(grau):
    if grau == 'Bacharelado':
        return 1
    elif grau == 'Licenciatura':
        return 2
    elif grau == 'Tecnológico':
        return 3
    elif grau == 'Bacharelado e Licenciatura':
        return 4
    else:
        return 0
    
st.title('Ferramenta de Previsão de Evasão')

# Sidebar setup
st.sidebar.title('🗂 Carregue o Arquivo')
upload_file = st.sidebar.file_uploader('Carregue um arquivo para fazer a previsão')
st.sidebar.write("O arquivo deve conter as seguintes informações: ano atual, carga horária \
integral, carga horária total, quantos anos despendidos no curso, o turno do curso, idade \
do aluno, raça/cor do aluno, grau acadêmico, categoria administrativa e categoria da \
organização acadêmica.")

if upload_file is not None:
    bytes_data = upload_file.getvalue()
    stringio = StringIO(upload_file.getvalue().decode("utf-8"))
    # To read file as string:
    string_data = stringio.read()
    dataframe = pd.read_csv(upload_file)
    st.write('Tabela de dados carregados, mostrando apenas as 5 primeiras linhas')
    st.dataframe(dataframe.head(5))
    predict = st.sidebar.button(label='Prever Evasão')
    
    if predict:
        mostrar_resultado_previsoes(dataframe)
else:
    st.write('Carregue uma base de dados ao lado para prever a evasão de um grupo \
        de alunos ou preencha as informações abaixo para prever individualmente.')
    c1, c2 = st.columns(2)
    NU_ANO_CENSO = 2019
    with c1:
        TP_CATEGORIA_ADMINISTRATIVA = st.selectbox('Qual a categoria administrativa da instituição de ensino?', 
            ["Pública Federal",
            "Pública Estadual",
            "Pública Municipal",
            "Privada com fins lucrativos",
            "Privada sem fins lucrativos",
            "Outros"])
        TP_ORGANIZACAO_ACADEMICA = st.selectbox('Qual a categoria \
            da organização acadêmica?', 
            ["Universidade",
             "Centro Universitário",
            "Faculdade",
            "Instituto Federal de Educação, Ciência e Tecnologia",           
            "Centro Federal de Educação Tecnológica"])
        QT_CARGA_HORARIA_INTEG = st.number_input('Qual a carga horária integral do curso?')
        QT_CARGA_HORARIA_TOTAL = st.number_input('Qual a carga horária total do curso?')
    with c2:
        NU_ANO_INGRESSO = st.number_input('Em qual ano ingressou no curso?', max_value=2019, min_value=2000)
        NU_IDADE = st.number_input('Qual a idade do aluno?', max_value=120, min_value=14)
        TP_COR_RACA = st.selectbox('Qual a cor/raça do aluno?', ['Não declarada', 'Branca', 'Preta', 'Parda', 'Amarela','Indígena', 'Sem informações'])
        TP_GRAU_ACADEMICO = st.selectbox('Qual o grau acadêmico do curso?', ['Bacharelado', 'Licenciatura', 'Tecnológico', 'Bacharelado e Licenciatura', 'Não aplicável'])
        TP_TURNO = st.selectbox('Qual o turno do curso?', ['Matutino', 'Vespertino', 'Noturno','Integral' ,'Não aplicável (EAD)'])
    predict = st.button(label='Prever Evasão')
    if predict:
        TP_TURNO = select_turno(TP_TURNO)
        NU_IDADE = NU_IDADE
        TP_GRAU_ACADEMICO = select_grau_academico(TP_GRAU_ACADEMICO)
        TP_COR_RACA = select_cor_raca(TP_COR_RACA)
        TP_CATEGORIA_ADMINISTRATIVA = select_categoria_administrativa(TP_CATEGORIA_ADMINISTRATIVA)
        TP_ORGANIZACAO_ACADEMICA = select_organizacao_academica(TP_ORGANIZACAO_ACADEMICA)
        ANOS_DESPENDIDOS = NU_ANO_CENSO - NU_ANO_INGRESSO
        dataframe = pd.DataFrame({
            'NU_ANO_CENSO': [NU_ANO_CENSO],
            'QT_CARGA_HORARIA_INTEG': [QT_CARGA_HORARIA_INTEG],
            'QT_CARGA_HORARIA_TOTAL': [QT_CARGA_HORARIA_TOTAL],
            'ANOS_DESPENDIDOS':[ANOS_DESPENDIDOS],
            'TP_TURNO':[TP_TURNO],
            'NU_IDADE':[NU_IDADE],
            'TP_COR_RACA':[TP_COR_RACA],
            'TP_GRAU_ACADEMICO':[TP_GRAU_ACADEMICO],
            'TP_CATEGORIA_ADMINISTRATIVA':[TP_CATEGORIA_ADMINISTRATIVA],
            'TP_ORGANIZACAO_ACADEMICA':[TP_ORGANIZACAO_ACADEMICA]
        }, index=['0'])
        mostrar_resultado_previsoes(dataframe)
        
#           