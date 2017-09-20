from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^$', views.about, name='about'),
	url(r'^contact/$', views.contact, name='contact'),
    url(r'^pet_status', views.pet_status, name='pet_status'),
    url(r'^pet/new/$', views.hatch_pet, name='hatch_pet'),
    url(r'^enter_BAL/$', views.change_pet_health_based_on_BAL, name='change_pet_health_based_on_BAL'),
    url(r'^incoming_sms/$', views.incoming_sms, name='views.incoming_sms'),
]