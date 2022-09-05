import streamlit as st
from PIL import Image

evaluation_model = Image.open("/Users/lais/Documents/Predict-Evasion-IT-Graduation/frontend/pages/evaluation.jpg")
st.set_page_config(
     page_title="Análise e Previsão de Evasão",
     page_icon=":shark:",
     layout="wide",
)

st.title('Sobre o Modelo Criado')
st.markdown("#### Imagem dos resultados de teste com o modelo")
st.image(evaluation_model, caption='Imagem da análise dos testes realizados no modelo atual')
st.markdown("#### Tabela de valores de F1-Score, Recall e Precision")