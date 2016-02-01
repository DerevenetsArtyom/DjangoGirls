from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^$', views.post_list),
    url(r'^post/(?P<post_id>[0-9]+)/$', views.post_detail),
]