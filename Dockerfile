FROM python:3.8

WORKDIR /projeto_evasao

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install --upgrade pip

COPY . .

# CMD ["uvicorn", "model_api:app", "--host", "0.0.0.0"]
CMD ["sh", "-c", "uvicorn model_api:app --host 0.0.0.0 --port 4000 && streamlit run Home.py --server.port 4000"]