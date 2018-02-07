from django.shortcuts import render

# Create your views here.

def rfa_home(request):
	
	current_rfa= Fact.objects.all()
	
	return render(request,'rfa/rfa_home.html',{'current_rfa': current_rfa} )
