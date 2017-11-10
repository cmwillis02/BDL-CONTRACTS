from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.franchise_list, name='franchise_list'),
	url(r'^franchise/(?P<pk>\d+)/$', views.franchise_detail, name= 'franchise_detail'),
	url(r'^player/(?P<pk>\d+)/$', views.player_detail, name= 'player_detail'),
	url(r'^update/(?P<pk>\d+)/$', views.ContractUpdate.as_view(), name= 'update_contract'),
]

