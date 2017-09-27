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
    return render(request, 'contracts/franchise_detail.html', {'franchise': franchise})	
    
def contract_new(request):
    
    form = ContractForm()
    return render(request, 'contracts/contract_new.html', {'form': form})
	