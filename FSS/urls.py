"""FSS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from apps.index.views import *
from apps.user.views import *
from apps.score.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('user/login/', enter),
    path('user/logout/', leave),
    path('user/regist/', reg),
    path('event/', event),
    path('team/', team),
    path('match/control/', control),
    path('match/scoring/', scoring),
    path('match/stream/', stream),
    path('match/data/', data),
    path('match/board/', board),
    path('match/referee/', referee),
    path('match/prepare/', prepare),
    path('match/result/', result),
]
