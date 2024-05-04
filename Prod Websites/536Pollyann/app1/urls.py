from django.contrib import admin
from  django.conf.urls import url
from django.conf.urls import include
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from app1 import views


urlpatterns =  [
        url('admin/', admin.site.urls),
        url(r'^$', views.home, name="home"),
        url(r'pictures', views.pictures, name="pictures"),
        url(r'ammenities', views.ammenities, name="ammenities"),
        url(r'location', views.location, name="location"),
        url(r'^sitemap', views.sitemap, name="sitemap"),
        url(r'^static/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG}),
        ]
