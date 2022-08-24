import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from lightgbm import LGBMClassifier

def generate_model():
    light_gbm = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("model", LGBMClassifier(class_weight='balanced'))
        ]
    )

    return light_gbm

def modeling(X_train, y_train):
    model = generate_model()
    return model.fit(X_train, y_train)
    