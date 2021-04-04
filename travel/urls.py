from django.contrib import admin
from django.urls import include, path,re_path
from . import views as indexview
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.static import serve 

urlpatterns = [
    path('', indexview.index),
    path('user/', include('user.urls')),
    path('forum/', include('forum.urls')),
    path('api/', include('api.urls')),
    path('movie/', include('movie.urls')),
    path('photo/', include('photo.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT,
        }),
    ]
#handler404 = views.page_not_found
#handler403 = views.permission_denied    
#handler500 = views.server_error