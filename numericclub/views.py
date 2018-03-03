from django.shortcuts import render
from django.http import HttpResponse

def rules(request):
    return render(request, 'rules.html', context)
