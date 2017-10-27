from django.contrib import admin
from .models import Franchise, Player, Contract

# Register your models here.

admin.site.register(Franchise)
admin.site.register(Player)

# Def admin class for contract registration

class ContractAdmin(admin.ModelAdmin):
	
	list_filter = ('current_ind','franchise_id')
	
admin.site.register(Contract, ContractAdmin)



