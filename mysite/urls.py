"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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

import main.views as main_views
import guestbook.views as guestbook_views

urlpatterns = [
    path('', main_views.index),
    path('user/login/', main_views.login),
    path('user/join/', main_views.join),
    path('user/modify/', main_views.modify),
    path('user/logout/', main_views.logout),
    path('guestbook/', guestbook_views.index),
    path('board/', main_views.board),


    path('guestbook/add', guestbook_views.add),
    path('guestbook/deleteform', guestbook_views.deleteform),
    path('guestbook/delete', guestbook_views.delete),
    path('admin/', admin.site.urls),

]
