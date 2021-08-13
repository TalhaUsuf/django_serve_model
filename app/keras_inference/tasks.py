# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                      write the actual prediction function
#   here which will only perform prediction
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



from app.celery import app
from . models import inference
import pandas as pd
from . apps import KerasInferenceConfig
import os
from rich.console import Console

from django.apps import AppConfig
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


Console().print(f"current dir is ---> {os.getcwd()}")


# @app.task(bind=True)
def run_prediction(self, model_obj_id): # id is integer value
    # see the serializers.py file
    current_obj_from_database = inference.objects.get(id=model_obj_id)
    # get the unique task-id of the current task which is being handled by celery
    # SEE https://docs.celeryproject.org/en/latest/faq.html?highlight=self.request.id#can-i-get-the-task-id-of-the-current-task

    current_obj_from_database.task_id = self.request.id # for celery # update the key value
    # inference.objects.filter(pk=model_obj_id).update(task_id=self.request.id)
    current_obj_from_database.save() # write the update to DataBase


    self.update_state(state='loaded the model', meta={'progress': 0})
    Console().print(f"attributes ====>>>", current_obj_from_database.__dict__)
    fields_list = [f.name for f in current_obj_from_database._meta.get_fields()]    # Console().print(f"attributes ====>>>", current_obj_from_database.objects)
    Console().print(f"fields list --> {type(fields_list)}, fields ==> {fields_list}")
    params = {k:getattr(current_obj_from_database, k) for k in fields_list}
    p = {}
    for k, v in params.items():
        p.setdefault(f'{k}', []).append(v)

    Console().print(f"printing the params : ==> \n {p}")
    del p['id'], p['task_id']
    Console().print(f"printing the params AFTER REMOVING ID KEY: ==> \n {p}")

    df = pd.DataFrame.from_dict(p)  # doesnot contain label field

    Console().print(f" data frame  is")


    out = KerasInferenceConfig.preprocess.transform(df)
    out = KerasInferenceConfig.model.predict(out).squeeze().tolist()
    Console().print(f"prediction -----> {out}")
    current_obj_from_database.prediction = out
    current_obj_from_database.save()
    Console().print(f"result saved to the DB")
    self.update_state(state='prediction ended', meta={'progress' : 100})

    return out