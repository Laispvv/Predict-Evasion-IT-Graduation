import imp
from io import StringIO
from unittest import result
import streamlit as st
import requests
import json
import pandas as pd

MODEL_URL = f'http://localhost:8000/predict'

st.set_page_config(
     page_title="Análise e Previsão de Evasão",
     page_icon=":shark:",
     layout="wide",
 )
# item = pd.DataFrame(data=[valor_v], columns=colunas_v)
# print(item.head())

def predict_results(url):
    result = requests.post(f"{url}", json={'text':'teste'})
    st.write("o resultado é:", json.loads(result.text)['prediction'][0])
    
# with st.form("my_ml"):
#     sentence = st.text_input(label="texto dsjhf")
#     modelo = st.radio("escolha:", ('1', '2'))
#     predict = st.form_submit_button(label='prever!')
#     predict_results(MODEL_URL)
st.title('Análise de Evasão Educacional')
st.markdown('Ferramenta de visualização de dados educacionais brasileiros de cursos de TI do ensino superior de 2009 à 2019.')
with st.container():
    tab1, tab2 = st.tabs(["📈 Análise de Dados", "🎯 Ferramenta de Previsão de Evasão"])
    with tab1:  
        st.markdown('### Ferramenta de Análise')
        col1, col2 = st.columns(2)
        with col1:
            st.radio('Selecione o sexo para análise:', ['Ambos', 'Homens', 'Mulheres'])
            st.multiselect('Estado', ['SC', 'SP', 'AC'])
            st.slider('Selecione os anos', 2009, 2019)
        with col2:
            st.slider('Faixa Etária', 15, 100)
            st.text_input('First name')
            st.multiselect('Instituição', ['Pública', 'Privada'])
            st.multiselect('Região', ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'])

    with tab2:
        st.markdown('### Ferramenta de Previsão de Evasão')
        uploaded_file = st.file_uploader("Escolha um arquivo")
        if uploaded_file is not None:
            # To read file as bytes:
            bytes_data = uploaded_file.getvalue()
            #  st.write(bytes_data)

            # To convert to a string based IO:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            #  st.write(stringio)

            # To read file as string:
            string_data = stringio.read()
            #  st.write(string_data)

            # Can be used wherever a "file-like" object is accepted:
            dataframe = pd.read_csv(uploaded_file)
            st.dataframe(dataframe.head(5))
            # predict = st.form_submit_button(label='prever!')
            # predict_results(MODEL_URL)
            
            
            
st.markdown('Desenvolvido por: Laís, Caroline, Luana, Euler, Nathália e Maria. 2022')

