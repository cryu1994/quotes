from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^success$', views.success),
    url(r'^add$', views.add),
    url(r'^show_user/(?P<user_id>\d+)$', views.view_user),
    url(r'^add_to_lists/(?P<id>\d+)$', views.add_to_my_list),
    url(r'^delete/(?P<id>\d+)$', views.destroy)
]
