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
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^registrationDeveloper/$', views.registrationDeveloper, name='registration_developer'),
    url(r'^registrationAdmin/$', views.registrationAdmin),
    url(r'^register/$', views.register),
    #url(r'^oauth/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^games/$', views.browse, name='browse'),
    url(r'^games/(?P<type>[-\w]+)/$', views.explore, name='explore'),
    url(r'^games/category/(?P<tag>[-\w]+)/$', views.explore_by_taxonomy, name='browse_by_category'),
    url(r'^games/tag/(?P<tag>[-\w]+)/$', views.explore_by_taxonomy, name='browse_by_tag'),
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^developer/$', views.developer, name='developer'),
    url(r'^game/(?P<slug>[-\w]+)/$', views.game_by_slug, name='game'),
    url(r'^payment/(?P<status>[-\w]+)/on/(?P<slug>[-\w]+)/$', views.payment, name='pay'),
    url(r'^api/(?P<target>[-\w]+)/$', views.api),
    url(r'^search/$', views.search, name='search'),
    url(r'^user/(?P<slug>[-\w]+)/$', views.game_by_slug, name='user_view'),
    url(r'^game/edit/([0-9]+)/$', views.edit_game, name='edit_game'),
    url(r'^game/delete/([0-9]+)/$', views.del_game, name='del_game'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
