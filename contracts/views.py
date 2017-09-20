from django.shortcuts import render

# Create your views here.

def franchise_list(request):
    return render(request, 'contracts/franchise_list.html', {})
