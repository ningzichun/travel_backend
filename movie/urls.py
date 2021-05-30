from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('new', views.newWork),
    path('<int:wid>/upload', views.uploadImage),
    path('<int:wid>/start', views.startWork),
    path('<int:wid>/status', views.getStatus),
    path('<int:wid>/delete', views.deleteMovie),
    path('<int:wid>/like', views.likeMovie),
    path('<int:wid>/comment', views.getComment),
    path('<int:wid>/comment/new', views.newComment),
    path('comment/<int:cid>/like', views.likeComment),
    path('comment/<int:cid>/delete', views.deleteComment),
    path('list', views.myMovieList),
    path('myall', views.myMovieListAll),
    path('all', views.movieListAll),
    path('tag/<int:tag>', views.movieListTag),
]
