from django.shortcuts import render
from .models import Franchise, Player, Contract
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from .forms import ContractForm

# Create your views here.
	
def franchise_list(request):
	
	franchises= Franchise.objects.all()
	return render(request,'contracts/franchise_list.html',{'franchises': franchises} )

def franchise_detail(request, pk):
    
    franchise = get_object_or_404(Franchise, pk= pk)
    active= Contract.objects.filter(current_ind= 'True').filter(franchise_id= pk).exclude(years= 0).order_by('years')
    pending= Contract.objects.filter(current_ind= 'True').filter(franchise_id= pk).filter(years= 0)
    
    
    return render(request, 'contracts/franchise_detail.html', {'franchise': franchise, 'active_players': active, 'pending_players' : pending})	
    
def player_detail(request, pk):
	
	contract = Contract.objects.filter(player_id = pk).order_by('-id')[0]
	
	return render(request, 'contracts/player_detail.html', {'contract' : contract})
	
class ContractUpdate(View):
	
	form_class= ContractForm
	model= Contract
	template_name= 'contracts/contract_new.html'
	
	def get_object(self, pk):
		
		return get_object_or_404(self.model, pk= pk)
		
	def get(self, request, pk):
		contract= self.get_object(pk)
		context= {'form' : self.form_class(instance= contract) , 'contract' : contract}
		
		return render(request, self.template_name, context)
		
	def post(self, request, pk):
		
		contract= self.get_object(id)
		bound_form= self.form_class(request.POST, instance= contract)
		
		if bound_form.is_valid():
			new_contract= bound_form.save()
			return redirect(new_contract)
		else:
			context= {'form': bound_form, 'contract' : contract}
			return render(request, self.template_name, context)
		
	
