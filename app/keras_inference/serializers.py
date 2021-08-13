from rest_framework import serializers
from . models import inference
from . tasks import  run_prediction

# create the serializer of the model inside the .models.py file

class inference_serializer(serializers.ModelSerializer):
    class Meta:
        model = inference
        fields = '__all__'

    # ALTHOUGH THE MODELSERIALIZER CLASS HAS BUILTIN DEFAULT IMPLEMENTATION FOR THE CREATE AND UPDATE METHODS
    # BUT HERE CREATE HAS BEEN OVERRIDDEN GIVEN THE REQUIREMENT THAT WE NOT ONLY WANT THE OBJECTS TO BE SAVED TO THE DATABASE
    # BUT ALSO WE WANT TO ASSIGN THE PREDICTION TASK TO CELERY WORKER BY PASSING THE PASSED IN DATA

    # create method here ensures that the model instance i.e. 'inference' is made and is saved to the database
    def create(self, validated_data): # viewsets have been used so this method is automatically called
        # when serializer.save() is called , it will execute what ever is inside this function
        '''create method inside serializer gets the validated data AND IT MUST RETURN MODEL OBJECT INSTANCES'''
        # create an entry in the database
        inference_obj = inference.objects.create(
            **validated_data)  # To create and save an object in a single step, use the create() method., SEE https://stackoverflow.com/questions/26672077/django-model-vs-model-objects-create
        # use the id keyword to get the respective row and perform inference
        run_prediction.delay(inference_obj.id) # innference.id gives the id corresponding to the current object added to the database

        return inference_obj


    def update(self, instance, validated_data):
        instance.email = validated_data.get('task_id', instance.task_id)
        instance.save()
        return instance