import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.express as px

st.set_page_config(
     page_title="Análise e Previsão de Evasão",
     page_icon=":shark:",
     layout="wide",
)

@st.cache(persist=True)
def load_data():
    data = pd.read_csv('../data/clean_data_2009_2019.csv', encoding='ISO-8859-1')
    return data

@st.cache(persist=True)
def soma_evasao_por_ano(data: pd.DataFrame, ano):
    result = data.loc[(data.NU_ANO_CENSO == ano)].groupby(['target']).size()
    return result

@st.cache(persist=True)
def soma_evasao_por_ano_valor(data: pd.DataFrame, ano, coluna, valor):
    print('valor:     ', valor)
    result = data.loc[(data.NU_ANO_CENSO == ano) & (data[coluna].isin(valor))].groupby(['target']).size()
    return result

@st.cache(persist=True)
def calcular_evasao_ano(data:pd.DataFrame, range_anos):
    contador = []
    anos = []
    sexo = []
    evasao = []
    evasao_tipo = ['Não Evadido', 'Evadido']
    for ano in range(range_anos[0], range_anos[1]+1):
        anos.append(ano)
        anos.append(ano)
        res = soma_evasao_por_ano(data, ano)
        contador.append(res[0])
        contador.append(res[1])
        evasao.append(evasao_tipo[0])
        evasao.append(evasao_tipo[1])
        
    df_retorno = pd.DataFrame({'Ano':anos, 'Evasao':evasao, 'Contador':contador})
    return df_retorno

@st.cache(persist=True)
def calcular_evasao_ano_sexo(data:pd.DataFrame, coluna, range_anos, coluna_label, range_valores, percentual = False):
    contador = []
    anos = []
    sexo = []
    evasao = []
    evasao_tipo = ['Não Evadido', 'Evadido']
    qt = len(coluna_label)
    for ano in range(range_anos[0], range_anos[1]+1):
        if qt == 2:
            res_col1 = soma_evasao_por_ano_valor(data, ano, coluna, range_valores[0])
            res_col2 = soma_evasao_por_ano_valor(data, ano, coluna, range_valores[1])
            for _ in range(qt*2):
                anos.append(ano)
            if percentual:
                total_mulheres = res_col1[0] + res_col1[1]
                total_homens = res_col2[0] + res_col2[1]
                contador.append(round((res_col1[0]/total_mulheres)*100, 2))
                contador.append(round((res_col1[1]/total_mulheres)*100, 2))
                contador.append(round((res_col2[0]/total_homens)*100, 2))
                contador.append(round((res_col2[1]/total_homens)*100, 2))
            else:
                contador.append(res_col1[0])
                contador.append(res_col1[1])
                contador.append(res_col2[0])
                contador.append(res_col2[1])
            
            for i in range(qt):
                for j in range(qt):
                    sexo.append(coluna_label[i])
                    evasao.append(evasao_tipo[j])
        else:
            # if coluna_label[0] == 'Mulher':
            res_col1 = soma_evasao_por_ano_valor(data, ano, coluna, range_valores[0])
            for _ in range(qt*2):
                anos.append(ano)
            if percentual:
                total = res_col1[0] + res_col1[1]
                contador.append(round((res_col1[0]/total)*100, 2))
                contador.append(round((res_col1[1]/total)*100, 2))
            else:
                contador.append(res_col1[0])
                contador.append(res_col1[1])
            sexo.append(coluna_label[0])
            sexo.append(coluna_label[0])
            evasao.append(evasao_tipo[0])
            evasao.append(evasao_tipo[1])
        print(len(evasao), len(anos), len(sexo), len(contador))
        
    df_retorno = pd.DataFrame({'Ano':anos, 'Evasao':evasao, 'Sexo':sexo,'Contador':contador})
    return df_retorno 

@st.cache
def parametros_grafico_sexo_evasao_sexo(sexo):
    if sexo == 'Todos':
        evasao_ano_sexo_df = calcular_evasao_ano_sexo(data, 'TP_SEXO', anos, coluna_label = ['Mulher', 'Homem'], range_valores=[[0], [1]], percentual=True)
    elif sexo == 'Mulheres':
        evasao_ano_sexo_df = calcular_evasao_ano_sexo(data, 'TP_SEXO', anos, coluna_label = ['Mulher'], range_valores=[[0]], percentual=True)
    else:
        evasao_ano_sexo_df = calcular_evasao_ano_sexo(data, 'TP_SEXO', anos, coluna_label = ['Homem'], range_valores=[[1]], percentual=True)
    return evasao_ano_sexo_df

@st.cache
def parametros_grafico_sexo_evasao_ies(ies):
    if ies == 'Todas':
        evasao_ano_ies_df = calcular_evasao_ano_sexo(data, 'TP_CATEGORIA_ADMINISTRATIVA', anos, coluna_label = ['Pública', 'Privada'], range_valores=[[1, 2, 3],[4, 5, 6, 7, 8, 9]])
    elif ies == 'Pública':
        evasao_ano_ies_df = calcular_evasao_ano_sexo(data, 'TP_CATEGORIA_ADMINISTRATIVA', anos, coluna_label = ['Pública'], range_valores=[[1, 2, 3]])
    else:
        evasao_ano_ies_df = calcular_evasao_ano_sexo(data, 'TP_CATEGORIA_ADMINISTRATIVA', anos, coluna_label = ['Privada'], range_valores=[[4, 5, 6, 7, 8, 9]])
    return evasao_ano_ies_df


def metricas(sexo):
    if sexo == 'Todos':
        cola, colb, colc, cold, cole, colf = st.columns(6)
        cola.metric("🧑‍🎓 Total de Estudantes", len(data))
        colb.metric('🚺 Mulheres', str( round((len(data.loc[data.TP_SEXO == 0])/len(data))*100, 2) ) + ' %')
        colc.metric('🚹 Homens', str( round((len(data.loc[data.TP_SEXO == 1])/len(data))*100, 2) ) + ' %')
        cold.metric("😁 Não Evadidos", str(round(len(data.loc[data.target == 0])/len(data), 2)*100) + " %")
        cole.metric("😢 Evadidos", str(round(len(data.loc[data.target == 1])/len(data), 2)*100) + " %")
        colf.metric("🥳 Idade Média", str(int(data.NU_IDADE.mean())) + ' anos')
    else:
        cola, colb, colc, cold = st.columns(4)
        cola.metric("🧑‍🎓 Total de Estudantes", len(data))
        colc.metric("😁 Não Evadidos", str(round(len(data.loc[data.target == 0])/len(data), 2)) + " %")
        colb.metric("😢 Evadidos", str(round(len(data.loc[data.target == 1])/len(data), 2)) + " %")
        cold.metric("🥳 Idade Média", str(int(data.NU_IDADE.mean())) + ' anos')

def select_data(data:pd.DataFrame, sexo, tipo_ies, anos, faixa_etaria):
    # filtro dos dados
    if sexo == 'Homens':
        data = data.loc[data.TP_SEXO == 1]    
    elif sexo == 'Mulheres':
        data = data.loc[data.TP_SEXO == 0]

    if tipo_ies == 'Pública':
        data = data.loc[data.TP_CATEGORIA_ADMINISTRATIVA.isin([1, 2, 3])]
    elif tipo_ies == 'Privada':
        data = data.loc[data.TP_CATEGORIA_ADMINISTRATIVA.isin([4, 5, 6, 7, 8, 9])]

    data = data.loc[(data.NU_ANO_CENSO <= anos[1]) & (data.NU_ANO_CENSO >= anos[0])]
    data = data.loc[(data.NU_IDADE <= faixa_etaria[1]) & (data.NU_IDADE >= faixa_etaria[0])]
    return data

data = load_data()
# sidebar
st.sidebar.title('⚙️ Configurações')
sexo =  st.sidebar.radio('Selecione o sexo para análise:', ['Todos', 'Homens', 'Mulheres'])
estado = st.sidebar.multiselect('Estado', ['SC', 'SP', 'AC'])
anos = st.sidebar.slider('Selecione os anos', 2015, 2019, (2015, 2019))
faixa_etaria = st.sidebar.slider('Faixa Etária', 15, 100, (15, 100))
tipo_ies = st.sidebar.radio('Tipo de Instituição', ['Todas', 'Pública', 'Privada'])
regiao = st.sidebar.multiselect('Região', ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'])

data = select_data(data, sexo, tipo_ies, anos, faixa_etaria)


container1, container2, container3 = st.container(),st.container(),st.container()
with container1:
    metricas(sexo)
        
with container2:
    # gráfico de linha, evasão por ano
    fig = px.line(calcular_evasao_ano(data, anos), x='Ano', y='Contador', color='Evasao', labels={'Evasao': ''}, title="Evasão total por ano")
    fig.update_xaxes(dtick=1)
    st.plotly_chart(fig, use_container_width=True)
        
with container3:
    col1, col2 = st.columns(2)
    with col2:
        # gráfico de barras, evasão por ano e tipo de instituição
        fig = px.bar(parametros_grafico_sexo_evasao_ies(tipo_ies), x='Ano', y='Contador', color='Sexo',  barmode='group', hover_data=['Evasao'], labels={'Sexo': ''}, text='Evasao', title='Evasão total por ano e sexo')
        fig.update_xaxes(dtick=1)
        st.plotly_chart(fig, use_container_width=True)
    with col1:
        # gráfico de barras, evasão por ano e sexo
        fig = px.bar(parametros_grafico_sexo_evasao_sexo(sexo), y='Ano', x='Contador', color='Sexo' , barmode='group', orientation='h',hover_data=['Evasao'], labels={'Sexo': '', 'Contador':'Contador (%)'}, text='Evasao', title='Evasão percentual por ano e sexo')
        fig.update_xaxes(dtick=20)
        st.plotly_chart(fig, use_container_width=True)

df = pd.DataFrame(
     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
     columns=['lat', 'lon'])

st.map(df)



