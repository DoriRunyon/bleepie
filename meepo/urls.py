from django.conf.urls import url
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, name='logout'),
    url(r'^accounts/password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
	url(r'^$', views.about, name='about'),
	url(r'^contact/$', views.contact, name='contact'),
    url(r'^pet_status', views.pet_status, name='pet_status'),
    url(r'^pet/new/$', views.hatch_pet, name='hatch_pet'),
    url(r'^enter_BAL/$', views.change_pet_health_based_on_BAL, name='change_pet_health_based_on_BAL'),
    url(r'^incoming_sms/$', views.incoming_sms, name='views.incoming_sms'),
]