from celery import Task
import logging
from app.celery import app
from celery import shared_task
# model imports
import copy
import os
import tensorflow as tf
import pandas as pd
from django.conf import settings
from pathlib import Path
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from rich.console import Console
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from rich.table import Table
from sklearn.compose import make_column_selector as selector
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras import backend as K
import joblib




class predict_task(Task):
    """
    Abstraction of Celery's Task class to support loading ML model.
    """
    abstract = True

    def __init__(self):
        super().__init__()
        self.model = None
        # to avoid sklearn pipeline errors
        self.numeric_transformer = None
        self.categorical_transformer = None
        self.preprocess_pipeline = None
        # ----------------------------------
        self.preprocess = None

    def __call__(self, *args, **kwargs):
        """
        Load model on first call (i.e. first task processed)
        Avoids the need to load model on each task request
        """
        if not self.numeric_transformer:
            self.numeric_transformer = Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler())
            ])
            logging.info("defined the numeric transformer")
        if not self.categorical_transformer:
            self.categorical_transformer = Pipeline([
                ("encoder", OneHotEncoder(handle_unknown="ignore"))
            ])
            logging.info("defined the categoric transformer")
        if not self.preprocess_pipeline:
            self.preprocess_pipeline = ColumnTransformer(transformers=[
                ("num", self.numeric_transformer, selector(dtype_exclude=object)),
                ("cat", self.categorical_transformer, selector(dtype_include=object))
            ])
            logging.info("setup preprocess_pipeline ... ")
        if not self.preprocess:
            self.preprocess = joblib.load((settings.PREPROCESSOR)) # see above comment
            logging.info("loded pre-processor from disk ....")
        if not self.model:
            logging.info('Defining model...')
            inp = tf.keras.Input(shape=(205))
            x = tf.keras.layers.Dense(10, activation=tf.nn.relu)(inp)
            x = tf.keras.layers.BatchNormalization()(x)
            x = tf.keras.layers.Dense(1024)(x)
            x = tf.keras.layers.BatchNormalization()(x)
            x = tf.keras.layers.Dense(1024)(x)
            x = tf.keras.layers.BatchNormalization()(x)
            out = tf.keras.layers.Dense(1, activation=tf.nn.sigmoid)(x)
            self.model = tf.keras.Model(inputs=[inp], outputs=[out])
            logging.info('Loading model ....')
            self.model.load_weights(settings.MODELS) # see the settings.py file which holds the paths to the model file and preprocessort file

            logging.info('Model loaded')
        return self.run(*args, **kwargs)


@app.task(  bind=True, # necessary argument, it means first arg will always be class instance
            ignore_result=False,
            base=predict_task,
            name=f"{__name__}")
def perform_prediciton(self, data:dict, db_id:int):
    features = copy.deepcopy(data)
    self.update_state(state=f"got features as input ... ")
    del features["task_id"] , features["id"], features["probability"]
    p = {}
    for key, value in features.items():
        p.setdefault(key, []).append(value)
    del features
    features = pd.DataFrame.from_dict(p)
    features = self.preprocess.transform(features)
    self.update_state(state=f"pre-procesing done on features ... ")
    prob = self.model.predict(features).squeeze().tolist()
    self.update_state(state=f"performed prediction ... ")

    return {'db_id':db_id, 'result':prob}  # get this in the GET method

