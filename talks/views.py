from django.shortcuts import render, get_object_or_404
from django.http import Http404

from .model import Talk

# Create your views here.

def archive(talk_id):
    talk_list = Talk.objects.all()
    return render(request, 'talks/archive.html', {'talk_list':talk_list})

def detail(talk_id):
    talk = get_object_or_404()
    return render(request, 'talks/detail.html', {'talk':talk})
