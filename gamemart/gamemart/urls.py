"""gamemart URL Configuration"""

from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import logout_then_login
from gameapp import views

urlpatterns = [
    url(r'^$', views.home, name='home_page'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^accounts/profile/$', views.home),
    #url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^logout/$', lambda request: logout_then_login(request, "/"), name='logout'),
    url(r'^registration/$', views.registration),
    url(r'^registrationDeveloper/$', views.registrationDeveloper),
    url(r'^registrationAdmin/$', views.registrationAdmin),
    url(r'^register/$', views.register),
    url(r'^oauth/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^games/$', views.browse),
    url(r'^games/(?P<type>[-\w]+)/$', views.explore, name='explore'),
    url(r'^games/category/(?P<tag>[-\w]+)/$', views.explore_by_taxonomy),
    url(r'^games/tag/(?P<tag>[-\w]+)/$', views.explore_by_taxonomy),
    url(r'^submit/$', views.submit),
    url(r'^game/([0-9]+)/$', views.game_by_id),
    url(r'^game/(?P<slug>[-\w]+)/$', views.game_by_slug, name='game_view'),
    url(r'^payment/(?P<status>[-\w]+)/on/(?P<slug>[-\w]+)/$', views.payment),
    url(r'^api/(?P<target>[-\w]+)/$', views.api),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
