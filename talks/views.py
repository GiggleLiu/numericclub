from django.shortcuts import render, get_object_or_404
from django.http import Http404

from .models import Talk, get_current_talk

# Create your views here.

def archive(request):
    talk_list = Talk.objects.all()
    return render(request, 'archive.html', {'talk_list':talk_list})

def current(request):
    talk = get_current_talk()
    if talk is not None:
        return render(request, 'detail.html', {'talk':talk})
    else:
        # no talk page.
        return render(request, 'notalk.html')

def detail(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)
    return render(request, 'detail.html', {'talk':talk})
