from django.shortcuts import render
from .models import Franchise, Player, Contract

# Create your views here.

def franchise_list(request):
	
	franchises= Franchise.objects.all()
	return render(request,'contracts/franchise_list.html',{'franchises': franchises} )
