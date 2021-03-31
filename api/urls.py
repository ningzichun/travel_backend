from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('color', views.getColorFunc),
    path('fsrcnn', views.FSRCNNFunc),
    path('weather', views.weatherFunc),
    path('location', views.getLocation),
    path('info', views.getInfo),
    path('poem', views.getPoem),
    path('test', views.getTest),
]
