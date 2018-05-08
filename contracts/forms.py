from django import forms
from .models import Contract
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS
from manage_db.src.util import mfl_api

class ContractForm(forms.ModelForm):

	class Meta:
		model = Contract
		fields = ['years']
    
	def __init__(self, status, franchise_id, pk, *args, **kwargs):
		super(ContractForm, self).__init__(*args, **kwargs)
		
		self.franchise_id = franchise_id
		self.status= status
        
	def clean_years(self):
		
		years= self.cleaned_data['years']
		
		franchise_total= Contract.objects.filter(franchise_id= self.franchise_id).filter(current_ind= 'True').aggregate(Sum('years_remaining'))
		current_roster_years= int(franchise_total['years_remaining__sum'])
		
		if years <= 0:
			raise ValidationError('Contract Error: Contracts must be 1 year or more')
		elif self.status == 'locked':
			raise ValidationError('Contract Error: Player is currently locked')
		elif years + current_roster_years > 50:
			raise ValidationError('Roster Error:  Contract will put roster over 50 year max')
		else:
			return years