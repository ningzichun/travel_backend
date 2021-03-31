from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('new', views.newWork),
    path('<int:wid>/upload', views.uploadImage),
    path('<int:wid>/start', views.startWork),
    path('<int:wid>/status', views.getStatus),
    path('<int:wid>/download', views.getMovie),
    path('<int:wid>/delete', views.deleteMovie),
    path('list', views.movieList),
    path('all', views.movieListAll),
]
