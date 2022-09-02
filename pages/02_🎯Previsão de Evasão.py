from io import StringIO
from unittest import result
import streamlit as st
import requests
import json
import pandas as pd

MODEL_URL = f'http://localhost:8000/predict'
replace_map = {
    'Resultado':{
        '0': 'Não evadido',
        '1': 'Evadido'
    }
}

def predict_results(url, value):
    result = requests.post(f"{url}", json=value)
    return json.loads(result.text)
    # st.write("o resultado é:", json.loads(result.text)['prediction'][0])

st.markdown('### Ferramenta de Previsão de Evasão')

# Sidebar setup
st.sidebar.title('🗂 Carregue o Arquivo')
upload_file = st.sidebar.file_uploader('Carregue um arquivo para fazer a previsão')

if upload_file is not None:
    # To read file as bytes:
    bytes_data = upload_file.getvalue()
    #  st.write(bytes_data)

    # To convert to a string based IO:
    stringio = StringIO(upload_file.getvalue().decode("utf-8"))
    #  st.write(stringio)

    # To read file as string:
    string_data = stringio.read()
    #  st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(upload_file)
    st.write('Tabela de dados carregados - 5 primeiras linhas')
    st.dataframe(dataframe.head(5))
    predict = st.sidebar.button(label='Prever Evasão')
    
    if predict:
        st.write('Resultado das previsões')
        result = predict_results(MODEL_URL, dataframe.to_json())
        # st.write(result)
        
        proba_evadir, proba_nao_evadir  = [], []
        for item in result['prediction_proba']:
            proba_nao_evadir.append(f'{round(item[0], 2)}%')
            proba_evadir.append(f'{round(item[1], 2)}%')
            
        result_df = pd.DataFrame({'Resultado':result['prediction'], 
                                  'Probabilidade Evadir':proba_evadir,
                                  'Probabilidade de Não Evadir': proba_nao_evadir})
        result_df.replace(replace_map)
        st.table(result_df)
    # predict_results(MODEL_URL)