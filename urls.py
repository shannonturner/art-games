from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from apps.mash.views import MashView, LearnView, MashFavoritesView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'art_games.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # Temporarily, the home page will be Art Mash
    url(r'^$', MashView.as_view(), name='home'),

    url(r'^(?:art/)?mash$', MashView.as_view(), name='mash'),
    url(r'^(?:art/)?learn$', LearnView.as_view(), name='learn'),
    url(r'^(?:art/)?favorites$', MashFavoritesView.as_view(), name='favorites'),
)
