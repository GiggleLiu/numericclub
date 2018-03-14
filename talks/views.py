from django.shortcuts import render, render_to_response
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.utils import timezone

from topics.models import Topic
from being.models import AdvancedUser
from .models import Talk, get_current_talk, headercontent4talk
from . import forms

# Create your views here.
def archive_user(request, pk):
    user = AdvancedUser.objects.get(pk=pk)
    talk_list = user.talk_set.all()
    return render(request, 'archive.html', {'talk_list':talk_list})

@login_required
def archive_me(request):
    return HttpResponseRedirect('/talks/user/%d/'%request.user.pk)

def current(request):
    talk = get_current_talk()
    if talk is not None:
        return HttpResponseRedirect('/talks/%d/'%talk.id)
    else:
        # no talk page.
        return render(request, 'notalk.html')

class ListView(generic.ListView):
    template_name = 'archive.html'
    context_object_name = 'talk_list'

    def get_queryset(self):
        return Talk.objects.all()

def talk_detail(request, pk):
    talk = Talk.objects.get(pk=pk)
    if talk.talk_date<timezone.now():
        talk.status = 2
        talk.save()
    header, content = headercontent4talk(talk)
    if talk is not None:
        return render(request, 'talk_detail.html',
                {'talk':talk, 'header':header, 'content':content})
    else:
        # no talk page.
        return render(request, 'notalk.html')

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
        if form.is_valid() and request.user == talk.user:
            data = form.cleaned_data
            # Save the user's form data to the database.
            talk.title = data['title']
            talk.talk_date = data['talk_date']
            talk.github_url = data['github_url']
            talk.save()
            headercontent4talk(talk, reload=True)
            return HttpResponseRedirect('/talks/%d/'%pk)
        else:
            error = form.errors
            talk = Talk.objects.get(pk=pk)
            # Render the template depending on the context.
            return render(request, 'talk_new.html',
                {'error': error, 'talk':talk, 'form':form, 'update':True})

@login_required
def talk_delete(request, pk):
    if request.method=='GET':
        talk = Talk.objects.get(pk=pk)
        if request.user == talk.user:
            talk.delete()
            return HttpResponseRedirect('/topics/list/')
        else:
            context = RequestContext(request)
            return render_to_response(
                'talk_new.html',
                {'error': 'You are not the owner to this talk!', 'form':form, 'update':True},
                context)

@login_required
def talk_publish(request, pk):
    talk = Talk.objects.get(pk=pk)
    if request.user == talk.user:
        talk.status = 1
        talk.save()
        return HttpResponseRedirect('/')
    else:
        return render(request, 'error.html',
            {'error': 'You are not the owner to this talk!'},)

@login_required
def talk_unpublish(request, pk):
    talk = Talk.objects.get(pk=pk)
    if request.user == talk.user or request.user.is_superuser:
        talk.status = 0
        talk.save()
        return HttpResponseRedirect('/')
    else:
        return render(request, 'error.html',
            {'error': 'You are not the owner to this talk or an admin!'},)
