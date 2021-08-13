from django.shortcuts import render
from . models import inference
from . serializers import inference_serializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from celery.result import AsyncResult
from rest_framework.response import Response
# Create your views here.
# views can be either created using low level APIView class or by using functional_views or by using view-sets which is a
# high level class with all the boiler plate code

class inferece_viewset(viewsets.ModelViewSet):
    # it inherits
    # mixins.CreateModelMixin,
    # mixins.RetrieveModelMixin,
    # mixins.UpdateModelMixin,
    # mixins.DestroyModelMixin,
    # mixins.ListModelMixin,
    # GenericViewSet
    # and mixins.CreateModelMixin has builtin serializers create method implemented
    # ModelViewSet class has already all the get post methods implemented
    queryset = inference.objects.all() # get multiple objects
    serializer_class = inference_serializer


    @action(detail=True, methods=["get"]) # make a custom routable action to be detecable by the router, True means single object will be passed
    def inference_progress(self, request, pk=None):
        # data = request.data  json as body
        # data = request.GET['username'] json as body
        '''this function is only for getting the progress regarding a single task'''
        inference_model_object = self.get_object() # get SINGLE object corresponding to the id
        # inference_model_object = inference.objects.get(pk) # get SINGLE object corresponding to the id

        # get_object implements thew following logic
        # def get_object(self):
        #     pk = int(self.kwargs['pk'])
        #     return get_object_or_404(BasicModel.objects.all(), id=pk)
        # get the latest object from database and get results
        result = AsyncResult(id=inference_model_object.task_id) # task_id is not attribute of model obj. see the tasks.py file for this
        progress = 100
        if isinstance(result.info, dict):
            progress = result.info["progress"]
        description = result.state

        return Response({
            "progress" : progress, "description" : description, "prediction" : result.get()}, status=status.HTTP_200_OK
        )
