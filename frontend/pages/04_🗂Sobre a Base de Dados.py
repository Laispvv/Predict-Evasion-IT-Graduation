import streamlit as st
from PIL import Image
import pandas as pd

st.set_page_config(
     page_title="Análise e Previsão de Evasão",
     page_icon=":shark:",
     layout="wide",
)

st.title('Sobre a Base de Dados')

st.markdown('## Da onde veio')
st.write("do inep")
st.markdown('## Filtros realizados')
st.write("Escolha de 2009 a 2019, apenas cursos de TI")
st.markdown('## Engenharia de Features')
st.write("o que fizemos, o que definiu a variável target?")