import streamlit as st
import requests
import json
import pandas as pd

st.set_page_config(
     page_title="Dropout Monitor",
     page_icon="🎓",
     layout="wide",
)

st.title('Análise de Evasão Educacional em Cursos de TI')
st.markdown('Ferramenta de visualização de dados educacionais brasileiros de cursos de TI do ensino superior de 2009 à 2019.')
            
st.markdown('Desenvolvido por: Laís, Caroline, Luana, Euler, Nathália e Maria. 2022')

