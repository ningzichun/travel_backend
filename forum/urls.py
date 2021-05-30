from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('page/<int:page_num>', views.getPage),
    path('post/new', views.newPost),
    path('post/<int:pid>', views.getPost),
    path('post/<int:pid>/edit', views.editPost),
    path('post/<int:pid>/delete', views.deletePost),
    path('post/<int:pid>/like', views.likePost),
    path('comment/new', views.newComment),
    path('comment/<int:cid>/delete', views.deleteComment),
    path('comment/<int:cid>/like', views.deleteComment),
    path('movie/', views.indexMovie),
]
