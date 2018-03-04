from django.shortcuts import render, render_to_response
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.utils import timezone

from topics.models import Topic
from .models import Talk, get_current_talk
from . import forms

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

class ListView(generic.ListView):
    template_name = 'archive.html'
    context_object_name = 'talk_list'

    def get_queryset(self):
        return Talk.objects.all()

class DetailView(generic.DetailView):
    model = Talk
    template_name = 'talk_detail.html'


@login_required
def talk_new(request, topic_id):
    if request.method=='GET':
        topic = Topic.objects.get(pk=topic_id)
        context = {'topic':topic, 'form':forms.NewTalkForm()}
        return render(request, 'talk_new.html', context)
    elif request.method=='POST':
        form = forms.NewTalkForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Save the user's form data to the database.
            user = request.user
            topic = Topic.objects.get(pk=topic_id)
            talk = Talk(topic=topic, user=user, title=data['title'], github_url=data['github_url'],
                    add_date=timezone.now(), talk_date=data['talk_date'])
            talk.save()
            return HttpResponseRedirect('/talks/%d/'%talk.id)
        else:
            context = RequestContext(request)
            error = form.errors
            topic = Topic.objects.get(pk=topic_id)
            # Render the template depending on the context.
            return render_to_response(
                'talk_new.html',
                {'error': error, 'form':form, 'topic':topic},
                context)

@login_required
def talk_update(request, pk):
    if request.method=='GET':
        talk = Talk.objects.get(pk=pk)
        context = {'topic':talk.topic, 'talk':talk,
                'form':forms.UpdateTalkForm(instance=talk), 'update':True}
        return render(request, 'talk_new.html', context)
    elif request.method=='POST':
        talk = Talk.objects.get(pk=pk)
        form = forms.UpdateTalkForm(data=request.POST, instance=talk)
        if form.is_valid():
            data = form.cleaned_data
            # Save the user's form data to the database.
            user = request.user
            talk.title = data['title']
            talk.talk_date = data['talk_date']
            talk.github_url = data['github_url']
            talk.save()
            return HttpResponseRedirect('/topics/%d/'%pk)
        else:
            context = RequestContext(request)
            error = form.errors
            # Render the template depending on the context.
            return render_to_response(
                'talk_new.html',
                {'error': error, 'form':form, 'update':True},
                context)

@login_required
def talk_delete(request, pk):
    if request.method=='GET':
        talk = Talk.objects.get(pk=pk)
        talk.delete()
        return HttpResponseRedirect('/topics/list/')
