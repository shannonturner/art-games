from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from apps.mash.views import MashView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'art_games.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # Temporarily, the home page will be Art Mash
    url(r'^$', MashView.as_view(), name='mash'),

    url(r'^mash', MashView.as_view(), name='mash'),
)
