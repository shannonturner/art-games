from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from apps.mash.views import HomeView, MashView, LearnView, MashFavoritesView, MashNoVotesView, UnlockedView
from apps.untitled.views import UntitledView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'art_games.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # Temporarily, the home page will be Art Mash
    url(r'^(?:art/)?$', HomeView.as_view(), name='home'),

    url(r'^(?:art/)?mash$', MashView.as_view(), name='mash'),
    url(r'^(?:art/)?learn$', LearnView.as_view(), name='learn'),
    url(r'^(?:art/)?favorites$', MashFavoritesView.as_view(), name='favorites'),
    url(r'^(?:art/)?novotes$', MashNoVotesView.as_view(), name='novotes'),
    url(r'^(?:art/)?untitled$', UntitledView.as_view(), name='untitled'),
    url(r'^(?:art/)?unlocked$', UnlockedView.as_view(), name='unlocked'),
)
