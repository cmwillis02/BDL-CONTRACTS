from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.franchise_list, name='contracts_home'),
	url(r'^franchise/(?P<pk>\d+)/$', views.franchise_contract_detail, name= 'franchise_contract_detail'),
	url(r'^contract/(?P<pk>\d+)/$', views.player_contract_detail, name= 'player_contract_detail'),
	url(r'^update/(?P<pk>\d+)/$', views.ContractUpdate.as_view(), name= 'update_contract'),
]

