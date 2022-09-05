import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.markdown('### Dashboard')

df = pd.read_csv('../data/df_2019_20.csv', encoding='ISO-8859-1')
st.session_state['df'] = df
data = df
# sidebar
st.sidebar.title('⚙️ Configuração dos gráficos')
sexo =  st.sidebar.radio('Selecione o sexo para análise:', ['Ambos', 'Homens', 'Mulheres'])
estado = st.sidebar.multiselect('Estado', ['SC', 'SP', 'AC'])
anos = st.sidebar.slider('Selecione os anos', 2009, 2019)
faixa_etaria = st.sidebar.slider('Faixa Etária', 15, 100)
tipo_ies = st.sidebar.multiselect('Tipo de Instituição', ['Pública', 'Privada'])
regiao = st.sidebar.multiselect('Região', ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'])

# st.write(data[['target', 'TP_SEXO', 'NU_ANO_CENSO']])

# gráficos
if sexo == 'Homens':
    data = data.loc[data.TP_SEXO == 2]

elif sexo == 'Mulheres':
    data = data.loc[data.TP_SEXO == 1]

chart = alt.Chart(data).mark_line().encode(
  x=alt.X('NU_ANO_CENSO:N'),
  y=alt.Y('target:Q'),
  color=alt.Color("TP_SEXO:N")
).properties(title="Evasão por sexo ao longo dos anos")
st.altair_chart(chart, use_container_width=True)
line = data[['target', 'TP_SEXO']].groupby(['target', 'TP_SEXO']).sum()

# st.dataframe(line)
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c']
     )

st.line_chart(chart_data)
