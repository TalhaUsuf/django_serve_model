from django.shortcuts import render
import json
from rest_framework.views import APIView
from detector.apps import DetectorConfig
from rest_framework import serializers
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rich.console import Console
from rest_framework import serializers

'''endpoint calls are directed to specific functions/classes in the views of our app'''
# Create your views here.






class validate_json(serializers.Serializer):
    path = serializers.ListField(child=serializers.CharField(required=True))
    # path = serializers.ListField(required=True)


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                for single instance of get method
#                           use this
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class call_model(APIView):

    parser_classes = [JSONParser] # converts query value to json request

    def __init__(self):
        print(dir(self))

    # means this will get be triggered on a get request
    def get(self, request):
        if request.method == 'GET': # ensures that request is parsed as json rather than query-value data


            try:
                # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                #                     validate the field
                # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                flag = validate_json(data=request.data)
                if flag.is_valid():
                # if True:

                    Console().rule("[red on yellow] got validated ...", align="left", style="green")

                    Console().print(f"[magenta] {request}")
                    # for getting the key from query
                    # params = request.GET.get('path')
                    params = request.data
                    Console().print(f"[cyan] type ===> {params}")
                    responses = [DetectorConfig.predictor.predict(i) for i in params['path']]
                    # response = DetectorConfig.predictor.predict(params['path'])

                    return JsonResponse({"features": responses,
                                         "n_preds" : len(responses),
                                         "validated" : "True"})

            except Exception as e:
                return HttpResponse(f"<html><body> Error encountered{e} </body></html>")






# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                     for multiple get calls against a single
#            request
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
# from rest_framework import viewsets
# from rest_framework.decorators import detail_route
# from rest_framework.response import Response
#
# class MyViewSet(viewsets.GenericViewSet):
#
#     @detail_route(methods=['get'])
#     def some_get_method(self, request, pk=None):
#         return Response({'data': 'response_data'})
#


