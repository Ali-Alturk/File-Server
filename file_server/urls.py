"""
URL configuration for file_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# urls.py (main)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from master.views import register_user, token_obtain
from file_server_app.views import FileUploadViewSet

router = DefaultRouter()
router.register(r'files', FileUploadViewSet)

urlpatterns = [
    path('api/register/', register_user, name='register'),
    path('api/token/', token_obtain, name='token_obtain'),
    path('api/', include(router.urls)),
]


