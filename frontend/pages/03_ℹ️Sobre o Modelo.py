import streamlit as st
from PIL import Image
import pandas as pd

st.set_page_config(
     page_title="Dropout Monitor",
     page_icon="🎓",
     layout="wide",
)

evaluation_model = Image.open("./frontend/pages/evaluation.png")

st.title('Sobre o Modelo Criado')
st.markdown("O modelo escolhido para realizar a classificação foi o **LightGBM** por ter apresentado \
     os melhores resultados entre todos os testados. Como parâmetros utillizados para ele, apenas \
     a escolha do peso das classes foi customizada, visto que o problema possuia um desbalanceamento \
     entre as classes evadido e não evadido.")
st.markdown("### Resultados")
st.markdown("Abaixo, é possível ver os resultados obtidos pelo modelo. Aqui, vale ressaltar que \
     por questões de negócio, foi priorizado maximizar os acertos dos alunos evadidos em \
     detrimento dos não evadidos, pois entende-se que com isso aqueles que usarem o sistema \
     poderiam prever possíveis evasões e agir com antecedência para tentar evitar, aplicando \
     as ações pedagógicas necessárias para dar suporte ao estudante e evitar que a evasão ocorra.")
st.image(evaluation_model, caption='Imagem da análise dos testes realizados no modelo atual')
st.markdown("Na tabela abaixo, foram calculados os valores para cada métrica, sendo que a \
     **acurácia foi de 89%**. Como citado anteriormente, o modelo foi escolhido de forma a \
     maximizar o F1-Score dos evadidos, obtendo como melhor resultado, uma taxa de 76% de acerto.")

data_results = pd.DataFrame({'Precision':[0.88, 0.71], 'Recall':[0.82, 0.81], 'F1-Score':[0.85, 0.76]}, index=['Não evadidos', 'Evadidos'])
# data_results = data_results.apply(lambda x : round(x*100))
st.table(data_results)