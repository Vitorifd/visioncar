from django.urls import re_path

from . import views  

urlpatterns = [
    re_path(r'^logs/(?P<car_plate>[A-Za-z0-9]{7})/$', views.log_create),
]
