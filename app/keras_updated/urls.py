from django.urls import path
from . views import predict_view, read_the_db, get_by_id
from rest_framework import routers
from django.conf.urls import include

app_name = "predict"



urlpatterns = [
    path("predict/", predict_view.as_view()),

    # path('get_data/<int:pk>', read_the_db.as_view()),
    path('db_get_all/', read_the_db.as_view()),
    path('db_get_id/<int:pk>', get_by_id.as_view()),
]