import json
from fastapi import FastAPI, Request
import pickle
import pandas as pd

with open("models/model.pkl", "rb") as file:
    model = pickle.load(file)

app = FastAPI()


@app.post("/predict")
async def predict(item: Request):
    request = await item.json()
    data = pd.read_json(request)
    data.drop(columns=['target'], inplace=True)
    pred = model.predict(data)
    pred_proba = model.predict_proba(data)
    return {"prediction": pred.tolist(), "prediction_proba": pred_proba.tolist()}

