from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from celery.result import AsyncResult
# Create your views here.
from .serializers import predict_serializer
from .models import predict
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import perform_prediciton
import io
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.decorators import api_view



class predict_view(APIView):

    def post(self, request, format=None):
        # GET JSON REQUEST ---> SAVE TO DATABASE ---> CALL CELERY WORKER ---> GET TASK-ID ---> SAVE TO DATABASE ---> RESPONSE THE TASK-ID
        # validate the request
        serializer = predict_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # write to the database , task-id and probability fields need to be written later
            # obj = predict.objects.create(**serializer.data)
            # current_id = obj.id
            current_id = serializer.data["id"]
            print(f"ID of the object added is : ===> {current_id}")
            #     call the celery worker
            celery_task_id = perform_prediciton.delay(data=serializer.data,
                                                      db_id=current_id)  # .data --> gives dictionary
            # predict.objects.filter(pk=current_id).update(task_id='sdgfdgdfgdfg')
            current_obj = predict.objects.get(pk=current_id)
            current_obj.task_id = celery_task_id  # modify the task id
            current_obj.save()  # save to database

            # serializer.save()
            # update the task_id field to database
            return Response({'db_obj_id': current_id, 'task_id': f'{celery_task_id}', 'status': 'Assigned to worker'},
                            status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if request.method == 'GET':
            task_id = request.GET.get('task_id', '')  # get the task_id query from user
            task = AsyncResult(task_id)  # get task result object
            if not task.ready():

                return Response({'task_id': task_id, "status": "Processing"}, status=status.HTTP_202_ACCEPTED)
            # because the relevant field needs to be updated in the database so db_obj_id is necessary to be returned by the task.py script
            else:
                #                 if task is ready
                result = task.get()
                db_id = result["db_id"]
                output = result["result"]
                # access the relevant object at database and update prediction field
                db_obj = predict.objects.get(pk=db_id)
                db_obj.probability = output
                db_obj.save() # write to the db

                return Response({"db_obj_id" : db_id, "task_id" : task_id, "status": "Completed", "result" : output})

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#           for checking heart beat
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# class check_heartbeat(viewsets.GenericViewSet):
#
#     @action(methods=['GET'], detail=True)
#     def heartbeat(self, request):
#         return Response({"alive":"OK"}, status=status.HTTP_200_OK)
    
@api_view(["GET"])
def check_heartbeat(request):
    if request.method=='GET':
        return Response({"heartbeat" : "OK"}, status=status.HTTP_200_OK)
    else:
        return Response({"status" : "this is a get method"}, status=status.HTTP_400_BAD_REQUEST)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#          for accessing the database stored items
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

class read_the_db(ListAPIView):
    queryset = predict.objects.all()
    serializer_class = predict_serializer


class get_by_id(RetrieveAPIView):
    queryset = predict.objects.all()
    serializer_class = predict_serializer
