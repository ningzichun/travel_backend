from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('new', views.newWork),
    path('<int:wid>/upload', views.uploadImage),
    path('<int:wid>/start', views.startPhoto),
    path('<int:wid>/status', views.getStatus),
    path('<int:wid>/delete', views.deletePhoto),
    path('<int:wid>/share', views.sharePhoto),
    path('list', views.myPhotoList),
    path('myall', views.myPhotoListAll),
    path('all', views.photoListAll),
]
