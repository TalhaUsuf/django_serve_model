from celery import shared_task, Celery
from apps import DetectorConfig
from django.shortcuts import render
import json
from rest_framework.views import APIView
from apps import DetectorConfig as PREDICT
from rest_framework import serializers
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rich.console import Console
from rest_framework import serializers
from detection_model import resnet_feature_extractor


app = Celery('tasks', broker='pyamqp://guest@localhost//', backend='rpc://')

# @shared_task(ignore_result=False)
# def add(x, y):
#     return {"result" : x+y}


@shared_task(ignore_result=False)
def predict(x):
    m = resnet_feature_extractor
    out = m.predict(x).cpu().squeeze().list()
    return out
