import streamlit as st
import requests
import json
import pandas as pd

st.set_page_config(
     page_title="Análise e Previsão de Evasão",
     page_icon=":shark:",
     layout="wide",
)

st.title('Análise de Evasão Educacional')
st.markdown('Ferramenta de visualização de dados educacionais brasileiros de cursos de TI do ensino superior de 2009 à 2019.')
            
st.markdown('Desenvolvido por: Laís, Caroline, Luana, Euler, Nathália e Maria. 2022')

