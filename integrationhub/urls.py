from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.landing, name="integration-hub"),
    path('admin/', admin.site.urls),
    path('mojaloops/', include('mojaloops.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)