from django.shortcuts import render, redirect
from .models import Franchise, Player, Contract
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, RedirectView
from .forms import ContractForm
from django.urls import reverse
from manage_db.src.util import mfl_api
from manage_db.src import main_rosters

	
def franchise_list(request):
	
	franchises= Franchise.objects.all()
	
	return render(request,'contracts/franchise_list.html',{'franchises': franchises} )

def franchise_contract_detail(request, pk):
    
    franchise = get_object_or_404(Franchise, pk= pk)
    active= Contract.objects.filter(current_ind= 'True').filter(franchise_id= pk).exclude(years_remaining= 0).exclude(roster_status= 'i').order_by('years_remaining')
    pending= Contract.objects.filter(current_ind= 'True').filter(franchise_id= pk).filter(years_remaining= 0)
    ir= Contract.objects.filter(current_ind= 'True'). filter(franchise_id= pk).filter(roster_status= 'i')
    
    active_count= Contract.objects.filter(current_ind= 'True').filter(franchise_id= pk).exclude(roster_status= 'i').count()
    ir_count= Contract.objects.filter(current_ind= 'True').filter(franchise_id= pk).filter(roster_status= 'i').count()
    
    roster_check= []
    if active_count > 25:
    	roster_check.append('Cannot assign contracts with > 25 active players')
    if ir_count > 3:
    	roster_check.append('Cannot assign contracts with > 3 IR players')
    
    return render(request, 'contracts/franchise_contract_detail.html', {'franchise': franchise, 'active_players': active, 'pending_players' : pending, 'ir' : ir, 'roster_check' : roster_check})	
    
def player_contract_detail(request, pk):
	
	contract = Contract.objects.filter(id = pk).order_by('-id')[0]
	
	return render(request, 'contracts/player_contract_detail.html', {'contract' : contract})
	
class ContractUpdate(View):
	
	form_class= ContractForm
	model= Contract
	template_name= 'contracts/contract_new.html'
	franchise_id= None
	
	def get_object(self, pk):
		
		return get_object_or_404(self.model, pk= pk)
			
	def set_status(self, pk):
		
		contract= self.get_object(pk)
			
		mfl_obj= mfl_api.export()
		return mfl_obj.game_status(contract.player_id)
	
	def get(self, request, pk):
		
		contract= self.get_object(pk)
		
		status= self.set_status(pk)
		
		self.franchise_id = contract.franchise_id
		context= {'form' : self.form_class(instance= contract,status= status, franchise_id= self.franchise_id, pk= pk) ,  'contract' : contract}
		
		return render(request, self.template_name, context)
		
	def post(self, request, pk):
	
		status= self.set_status(pk)
		
		contract= self.get_object(pk)
		bound_form= self.form_class(status, contract.franchise_id,pk, request.POST, instance= contract)

		if bound_form.is_valid():
			contract.years_remaining= contract.years
			bound_form.save()
			
			mfl_obj= mfl_api._import()
			mfl_obj.import_contract(contract.player_id, contract.years)
			
			mfl_obj.import_message_board('Player {} assigned new {} year(s) contract'.format(contract.player_id, contract.years))
			
			return redirect(reverse('franchise_contract_detail', kwargs= {'pk' : contract.franchise_id}))
			
		else:
			context= {'form': bound_form, 'contract' : contract}
			return render(request, self.template_name, context)
			

		
	
