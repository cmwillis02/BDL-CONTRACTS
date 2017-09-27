from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.franchise_list, name='franchise_list'),
	url(r'^contracts/franchise/(?P<pk>\d+)/$', views.franchise_detail, name='franchise_detail'),
	url(r'^contracts/new/$', views.contract_new, name= 'contract_new')
]
