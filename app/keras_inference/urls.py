# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                      urls for keras_inference app   
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


from django.contrib import admin
from django.urls import path
from .views import inferece_viewset
from rest_framework import routers
from django.urls import path
from django.conf.urls import include


router = routers.DefaultRouter()

router.register('keras_inference', inferece_viewset)


urlpatterns = [
    path('', include(router.urls)),
]
