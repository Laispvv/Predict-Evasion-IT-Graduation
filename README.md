# Predict-Evasion-IT-Graduation
Data pipeline from data cleaning to model training for creating a model to predict evasion on brazilian's IT graduation courses from 2015 to 2019

## Passo a passo para execução

1. Criar e ativar um ambiente virtual, inicie o ambiente com o python 3.8
   1. ```python3 -m venv <nome_venv>```
   2. ```source <nome_venv>/bin/activate```
2. Instalar os requirements
   1. ```pip install -r requirements.txt```
3. Rodando o Docker
   1. ```docker build . -t <tag_name>```
   2. ```docker run -p 8000:8000 <tag_name>```, com esse comando, direciona todas as requisições que chegam na porta 8000 da minha máquina para a porta 8000 do container.
4. Rodando o Streamlit: ```streamlit run Home.py```
5. Rodando o FastAPI: ```uvicorn model_api:app```
6. Rodando no Macbook: para instalar o Lightgbm, primeiro é preciso instalar `brew cmake` e `brew libomp`



