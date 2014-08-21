from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from views import index , emotion

urlpatterns = patterns('',
    (r'^index/$',index),
    (r'^emotion/$',emotion),
    # Examples:
    # url(r'^$', 'tweet_sentiment_vis.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)


