from django import forms
from .models import Contract
from django.db.models import Sum
from django.core.exceptions import ValidationError

class ContractForm(forms.ModelForm):

	class Meta:
		model = Contract
		fields = ['years']
    
	def __init__(self, franchise_id, *args, **kwargs):
		super(ContractForm, self).__init__(*args, **kwargs)
    	
		self.franchise_id = franchise_id
        
	def clean_years(self):
		years= self.cleaned_data['years']
		
		
		
		franchise_total= total_years= Contract.objects.filter(franchise_id= self.franchise_id).filter(current_ind= 'True').aggregate(Sum('years_remaining'))
		current_roster_years= int(franchise_total['years_remaining__sum'])
		
		if years <= 0:
			raise ValidationError('Contract Error: Contracts must be 1 year or more')
		
		elif years + current_roster_years > 50:
			raise ValidationError('Roster Error:  Contract will put roster over 50 year max')
		else:
			return years