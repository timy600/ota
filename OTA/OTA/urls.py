from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # path('', include('crs.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('crm.urls')),
]