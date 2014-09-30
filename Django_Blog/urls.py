from django.conf.urls import url

from blog import views

urlpatterns=[
             url(r'^login/$', views.login),
             url(r'^signup/$',views.signup),
             url(r'^search/$',views.search),
             url(r'^userr/$',views.userr),
             url(r'^create/$',views.create),
             url(r'^(?P<context>[0-9]+)/blog/$',views.blog,name='blog'),
             url(r'^(?P<context>[0-9]+)/create/$',views.create,name='create'),
             url(r'^(?P<context>[0-9]+)/reply/$',views.reply,name='reply'),
             url(r'^(?P<context>[0-9]+)/(?P<context1>[0-9]+)/dele/$',views.dele,name='dele'),
            ]
