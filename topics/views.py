from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import get_topics_ranked, Genre, Topic, newvote

def topic_list(request):
    glist = Genre.objects.all()
    tlist = []
    for g in glist:
        tl = get_topics_ranked(g)
        like = [sum([v.kind==1 for v in t.vote_set.all()]) - sum([v.kind==2 for v in t.vote_set.all()]) for t in tl]
        talk = [sum([v.kind==0 for v in t.vote_set.all()]) for t in tl]
        tlist.append(zip(tl, like, talk))
    context = {
            'topic_list':zip(glist, tlist),
            }
    return render(request, 'topic_list.html', context)

@login_required
def vote(request, topic_id, kind):
    user = request.user
    topic = Topic.objects.get(pk=topic_id)
    newvote(user, topic, kind=kind)
    return HttpResponseRedirect('/topics/list/')

def topic_detail(request, topic_id):
    t = Topic.objects.get(pk=topic_id)
    like_list, dislike_list, talk_list = [], [], []
    for v in t.vote_set.all():
        if v.kind == 0:
            talk_list.append(v.user)
        elif v.kind==1:
            like_list.append(v.user)
        else:
            dislike_list.append(v.user)
    context = {
            'topic': t,
            'like_list': like_list,
            'dislike_list': dislike_list,
            'talk_list': talk_list,
            }
    return render(request, 'topic_detail.html', context)


