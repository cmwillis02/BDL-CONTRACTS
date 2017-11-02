from django.shortcuts import render
from .models import Franchise, Player, Contract
from django.shortcuts import render, get_object_or_404
from .forms import ContractForm

# Create your views here.
	
def franchise_list(request):
	
	franchises= Franchise.objects.all()
	return render(request,'contracts/franchise_list.html',{'franchises': franchises} )

def franchise_detail(request, pk):
    
    franchise = get_object_or_404(Franchise, pk=pk)
    active= Contract.objects.filter(current_ind = 'True').filter(franchise_id = pk).order_by('years')
    
    
    return render(request, 'contracts/franchise_detail.html', {'franchise': franchise, 'active_players': active})	
    
def player_detail(request, pk):
	
	contract = Contract.objects.filter(player_id = pk).order_by('-id')[0]
	
	return render(request, 'contracts/player_detail.html', {'contract' : contract})
	
