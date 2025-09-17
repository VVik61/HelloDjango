from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('myapp.urls')),
    path('', include('core.urls')),
    path('myapp/', include('myapp.urls')),
    path('users/', include('users.urls')),
    path('messaging/', include('messaging.urls')),
    path('anketa/', include('anketa.urls')),
    path('account/login/', LoginView.as_view(template_name='users/login.html'), name='login'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

