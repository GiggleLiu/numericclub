from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect

from . import forms
from .models import *

def user_detail(request, user_id):
    if request.method == 'GET':
        context = RequestContext(request)
        objuser = AdvancedUser.objects.get(pk=user_id)
        return render(request, 'user_detail.html', {'objuser': objuser})

@csrf_exempt
def login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        # check that the test cookie worked.
        user = auth.authenticate(email=request.POST.get(
            'email'), password=request.POST.get('password'))
        if user:
            if user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
            else:
                return render_to_response('error.html', {'error': 'your account is no longer active!'}, context)
        else:
            print('authentication failure')
            return render_to_response('error.html', {'error': 'Password incorrect!'}, context)

    return render_to_response('index.html', context)


def register_success(request):
    context = RequestContext(request)
    return render_to_response('success.html', {'content': 'succeed!'}, context)

def register(request):
    # Like before, get the request's context.
    if request.method == 'GET':
        user_form = forms.NewUserForm()
        return render(request, 'user_update.html', {'form': user_form})

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = forms.NewUserForm(request.POST, request.FILES)

        # If the two forms are valid...
        if user_form.is_valid():
            data = user_form.cleaned_data
            user = newuser(
                truename=data['truename'], email=data['email'], avatar=data['avatar'],
                password=data['password'], description=data['description'])
            request.session['user_id'] = user.id

            # Update our variable to tell the template registration was successful.
            return HttpResponseRedirect('/being/register_success/')

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            error = user_form.errors
            # Render the template depending on the context.
            return render(request, 'user_update.html', {'error': error, 'form':user_form})


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

@login_required
def user_update(request):
    # Like before, get the request's context.
    if request.method == 'GET':
        form = forms.UpdateUserForm(instance=request.user)
        return render(request, 'user_update.html', {'form': form, 'update': True})

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user = request.user
        user_form = forms.UpdateUserForm(request.POST, request.FILES, instance=user)

        # If the two forms are valid...
        if user_form.is_valid():
            data = user_form.cleaned_data
            # Save the user's form data to the database.
            updateuser(user, data['description'], data['avatar'])
            # Update our variable to tell the template registration was successful.
            return HttpResponseRedirect('/being/user_detail/' + str(user.id))
        else:
            error = user_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        error = 'Error accur'

    # Render the template depending on the context.
    return render_to_response(
        'user_update.html',
        {'error': error, 'form':form},
        context)

@csrf_exempt
@login_required
def update_password(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = forms.UpdatePasswordForm(request.POST, request.FILES)
        if form.is_valid():
            old = request.POST.get('oldpassword')
            new = request.POST.get('newpassword')
            # Save the user's form data to the database.
            if user:
                updatepassword(user, old, new)
                auth.login(request, user)
                # Update our variable to tell the template registration was successful.
                return HttpResponseRedirect('/being/user_detail/' + str(user.id))
            else:
                error = 'initial password incorrect!'

        else:
            error = 'invalid form, please check your input.'
    else:
        # Render the template depending on the context.
        form = forms.UpdatePasswordForm()
        return render(request, 'update_password.html', {'form': form})

    # Render the template depending on the context.
    form = forms.UpdatePasswordForm()
    return render(request, 'update_password.html', {'error': error, 'form':form})


def user_delete(request):
    context = RequestContext(request)
    if request.method == 'GET':
        user = request.user
        deleteuser(user)
        return HttpResponseRedirect('/')
