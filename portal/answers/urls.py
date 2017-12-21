from django.conf.urls import url
from .views import *

app_name = 'answers'

urlpatterns = [
    url(r'^$', PublicContribListView.as_view(), name='index'),
    url(r'^create/$', PublicContribCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', PublicContribDetailView.as_view(), name='get'),
    url(r'^(?P<slug>[\w-]+)/edit/$', PublicContribUpdateView.as_view(), name='edit'),
    url(r'^(?P<slug>[\w-]+)/del/$', PublicContribDeletelView.as_view(), name='del'),
]