from . models import predict
from rest_framework import serializers






class predict_serializer(serializers.ModelSerializer): # create and update fields are present by default
    class Meta:
        model = predict
        fields = '__all__'


