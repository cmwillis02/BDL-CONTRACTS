from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.franchise_list, name='franchise_list'),
]