from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^join/$', views.JoinView.as_view(), name='join'),
    url(r'^(?P<pk>\d+)', views.user_view, name='user_view')
]
