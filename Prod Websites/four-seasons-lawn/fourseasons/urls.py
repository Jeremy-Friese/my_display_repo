from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import TemplateView
import django.views.static
from main import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^static/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG}),
    url('', include('main.urls', namespace="main")),
    url('terms', views.terms, name="terms"),
    url('thankyou', views.thankyou, name="thankyou"),
    url('payment', views.PaymentView.as_view(), name="payment"),
    url('services', views.services, name="services"),
    url('about', views.about, name="about"),
    url('privacy', views.privacy, name="privacy"),
    url('sitemap', views.sitemap, name="sitemap"),
    url(r'^robots', views.robots, name="robots"),
    url(r'^static/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG}),
    url('', views.home, name='main'),
]
