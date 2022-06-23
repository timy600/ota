"""CRM API URL Configuration
"""
from django.urls import include, path

urlpatterns = [
    path('user/', include('crm.apis.urls')),
]