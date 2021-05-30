from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('new', views.newPhoto),
    path('<int:wid>/upload', views.uploadImage),
    path('<int:wid>/start', views.startPhoto),
    path('<int:wid>/status', views.getStatus),
    path('<int:wid>/delete', views.deletePhoto),
    path('<int:wid>/like', views.likePhoto),
    path('<int:wid>/comment', views.getComment),
    path('<int:wid>/comment/new', views.newComment),
    path('comment/<int:cid>/like', views.likeComment),
    path('comment/<int:cid>/delete', views.deleteComment),
    path('list', views.myPhotoList),
    path('myall', views.myPhotoListAll),
    path('all', views.photoListAll),
]
