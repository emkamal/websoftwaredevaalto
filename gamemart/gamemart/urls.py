"""gamemart URL Configuration"""

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from gameapp import views

urlpatterns = [
    url(r'^$', views.home, name='home_page'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logged_out.html'}, name='logout'),
    url(r'^register/$', views.register),
    url(r'^browse/$', views.browse),
    url(r'^submit/$', views.submit),
    url(r'^game/([0-9]+)/$', views.gameview),
]
