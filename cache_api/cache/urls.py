from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index),
    path("put", views.put_api),
    path("get", views.get_api),
]