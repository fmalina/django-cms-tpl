from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'hon.cert.views.listing', name='recent'),
    url(r'^certify$', 'hon.cert.views.certify', name='certify'),
    url(r'^(?P<slug>[a-z-]+)$', 'hon.cert.views.listing', name='category'),
    url(r'^(?P<id>\d+)$', 'hon.cert.views.cert', name='cert'),
    url(r'^(?P<id>\d+)/edit$', 'hon.cert.views.edit_cert'),
    url(r'^thumb/(?P<url>.*)$', 'hon.cert.thumb.thumb', name='thumb'),
)