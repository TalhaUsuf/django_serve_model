from django.db import models
# all database related things go here

'''
Django web applications access and manage data through Python objects referred to as models.
 Models define the structure of stored data, including the field types and possibly also their maximum size, default values,
  selection list options, help text for documentation, label text for forms, etc. 
  The definition of the model is independent of the underlying database — 
you can choose one of several as part of your project settings. 
Once you've chosen what database you want to use, you don't need to talk to it directly at all — you just write 
your model structure and other code, and Django handles all the dirty work of communicating with the database for you.
'''


# Create your models here.
class widgets(models.Model):
    name = models.CharField(max_length=100)