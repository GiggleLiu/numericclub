from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views import generic

from .models import Talk, get_current_talk

# Create your views here.

def archive(request):
    talk_list = Talk.objects.all()
    return render(request, 'archive.html', {'talk_list':talk_list})

def current(request):
    talk = get_current_talk()
    if talk is not None:
        return render(request, 'talk_detail.html', {'talk':talk})
    else:
        # no talk page.
        return render(request, 'notalk.html')

def detail(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)
    return render(request, 'detail.html', {'talk':talk})

class ListView(generic.ListView):
    template_name = 'archive.html'
    context_object_name = 'talk_list'

    def get_queryset(self):
        return Talk.objects.all()

class DetailView(generic.DetailView):
    model = Talk
    template_name = 'talk_detail.html'
