from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils import timezone

from .models import get_topics_ranked, Genre, Topic, newvote
from . import forms

def topic_list(request):
    glist = Genre.objects.all()
    tlist = []
    for g in glist:
        tl = get_topics_ranked(g)
        tlist.append(tl)
    context = {
            'topic_list':zip(glist, tlist),
            }
    return render(request, 'topic_list.html', context)

@login_required
def vote(request, pk, kind):
    user = request.user
    topic = Topic.objects.get(pk=pk)
    newvote(user, topic, kind=kind)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    #return HttpResponseRedirect('/topics/list/')

class DetailView(generic.DetailView):
    model = Topic
    template_name = 'topic_detail.html'

@login_required
def topic_new(request, pk):
    if request.method=='GET':
        genre = Genre.objects.get(pk=pk)
        context = {'genre':genre, 'form':forms.NewTopicForm()}
        return render(request, 'topic_new.html', context)
    elif request.method=='POST':
        form = forms.NewTopicForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Save the user's form data to the database.
            user = request.user
            genre = Genre.objects.get(pk=pk)
            topic = Topic(genre=genre, user=user,text=data['text'], add_date=timezone.now())
            topic.save()
            return HttpResponseRedirect('/topics/%d/'%topic.id)

@login_required
def topic_update(request, pk):
    if request.method=='GET':
        topic = Topic.objects.get(pk=pk)
        context = {'genre':topic.genre, 'topic':topic, 'form':forms.UpdateTopicForm(instance=topic)}
        return render(request, 'topic_new.html', context)
    elif request.method=='POST':
        topic = Topic.objects.get(pk=pk)
        form = forms.UpdateTopicForm(data=request.POST, instance=topic)
        if form.is_valid():
            data = form.cleaned_data
            # Save the user's form data to the database.
            topic.text = data['text']
            topic.save()
            return HttpResponseRedirect('/topics/%d/'%pk)

@login_required
def topic_delete(request, pk):
    if request.method=='GET':
        if request.user.is_superuser:
            topic = Topic.objects.get(pk=pk)
            topic.delete()
            return HttpResponseRedirect('/topics/list/')
