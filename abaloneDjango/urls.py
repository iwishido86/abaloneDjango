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

from abaloneDjango.views import base_view, knight_login_view, knight_select_view, knight_auto_view, start_view, \
    join_view, assin_view, delete_view, init_view, mycard_view, expeditionSeq_ini_view, \
    game_complete_view, knight_election_view, knight_expedition_view, game_succ_view, game_fail_view, hosu_view, \
    hosu_show_view, hosu_select_view, honor_view

urlpatterns = [
    path('admin/', admin.site.urls),
#    path('api/auth/register/', registration_view, name='register_user'), # 추가
#    path('api/auth/login/', obtain_auth_token, name='login'), # 추가
    path('base/', base_view),
    path('knight_login/', knight_login_view),
    path('login/<str:username>/', knight_auto_view, name='knight_auto_view'), # 추가
    path('mycard/<str:username>/', mycard_view, name='mycard_view'), # 추가

    path('knight_select/', knight_select_view),
    path('knight_select/<str:username>/', knight_select_view, name='knight_select_view'), # 추가
    path('knight_election/<str:username>/', knight_election_view, name='knight_election_view'), # 추가
    path('knight_expedition/<str:username>/', knight_expedition_view, name='knight_expedition_view'), # 추가

    path('start/', start_view ,name='start_view'),
    path('join/<str:username>/', join_view ,name='join_view'),

    path('honor/<str:username>/', honor_view ,name='honor_view'),

    path('hosu/<str:username>/', hosu_view ,name='hosu_view'),
    path('hosu_show/<str:username>/', hosu_show_view ,name='hosu_show_view'),
    path('hosu_select/<str:username>/', hosu_select_view ,name='hosu_select_view'),

    path('delete/<str:username>/', delete_view ,name='delete_view'),
    path('assin/', assin_view ,name='assin_view'),
    path('init/', init_view ,name='init_view'),

    path('game_complete/<int:gameid>/', game_complete_view, name='game_complete_view'),
    path('game_succ/<int:gameid>/', game_succ_view, name='game_succ_view'),
    path('game_fail/<int:gameid>/', game_fail_view, name='game_fail_view'),
    path('expeditionSeq_ini/<int:gameid>/', expeditionSeq_ini_view, name='expeditionSeq_ini_view'),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
