from django.urls import path
from . views import predict_view, read_the_db, get_by_id
from . views import check_heartbeat
from rest_framework import routers
from django.conf.urls import include

# route = routers.SimpleRouter()
# route.register("heartbeat", check_heartbeat, basename="heartbeat")

app_name = "predict"



urlpatterns = [
    path("predict/", predict_view.as_view()),

    # path('get_data/<int:pk>', read_the_db.as_view()),
    path('db_get_all/', read_the_db.as_view()),
    path('db_get_id/<int:pk>', get_by_id.as_view()),
    # path(r'', include(route.urls))
    path('heartbeat', check_heartbeat)
]
