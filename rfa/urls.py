from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.rfa_home, name='rfa_home'),
]

