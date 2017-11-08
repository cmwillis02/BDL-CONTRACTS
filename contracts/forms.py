from django import forms
from .models import Contract
from django.db.models import Sum
from django.core.exceptions import ValidationError

class ContractForm(forms.ModelForm):

    class Meta:
        model = Contract
        fields = ['years']
        
        def clean_years(self):
        	data= self.cleaned_data['years']
        	current_roster_years= total_years= Contract.objects.filter(franchise_id= 8).filter(current_ind= 'True').Aggregate(Sum('years'))
        	
        	if int(data) + int(current_roster_years) > 50:
        		raise ValidationError('Roster Error:  Contract will put roster over 50 year max')
        		
        	if int(data) <= 0:
        		raise ValidationError('Contract Error: Contracts must be 1 year or more')
        		
        	return data