from django.shortcuts import render
from django.http import HttpResponse
from .models import get_topics_ranked, Genre, Topic

# Create your views here.
def index(request):
    return HttpResponse('Hello!')

def topic_list(request):
    s = ''
    glist = Genre.objects.all()
    tlist = []
    for g in glist:
        tlist.append(get_topics_ranked(g))
    context = {
            'glist':glist,
            'tlist':tlist,
            }
    return render(request, 'topics/list.html', context)

def vote(request, topic_id, kind):
    if request.method == 'POST':
        v = Vote(topic_id=topic_id, user_id=user_id, kind=kind)
        v.save()
        return HttpResponseRedirect('/topic/list/')
