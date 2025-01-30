from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.middleware.csrf import get_token
from django.http import JsonResponse

def get_csrf_token(request):
    token = get_token(request)
    response = JsonResponse({'csrfToken': token})
    response.set_cookie('csrftoken', token, httponly=False, samesite='None', secure=False)
    return response

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Static API Calls
    path('api/csrf/', get_csrf_token, name='get_csrf_token'),
    path('api/ltm/', include('f5_devices.urls')),
    path('api/build-ltm/', include('LTM.urls')),

    # Subnet Calculator
    path('sub-net/', include('subnetCalc.urls')),
    # Angular catch-all route (excluding static files)
    # re_path(r'^(?!static/).*$', TemplateView.as_view(template_name="browser/index.html")),
    re_path(r'^(?!api/).*$', TemplateView.as_view(template_name="browser/index.html")),
]

# Serve static files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
