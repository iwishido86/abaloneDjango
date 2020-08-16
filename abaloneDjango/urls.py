"""abaloneDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

from abaloneDjango.views import base_view, knight_login_view, knight_select_view, knight_auto_view

urlpatterns = [
    path('admin/', admin.site.urls),
#    path('api/auth/register/', registration_view, name='register_user'), # 추가
#    path('api/auth/login/', obtain_auth_token, name='login'), # 추가
    path('base/', base_view),
    path('knight_login/', knight_login_view),
    path('login/<str:username>/', knight_auto_view, name='knight_auto_view'), # 추가

    path('knight_select/', knight_select_view),
    path('knight_select/<str:username>/', knight_select_view, name='knight_select_view'), # 추가
    path('img/', knight_select_view),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
