
from django.shortcuts import render, redirect
from django.views import View
import requests
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
from django.template.loader import get_template
import simplejson as json
from pprint import pprint as pp

from django.shortcuts import render


def LogIn(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            input_username = form.cleaned_data['username']
            input_password = form.cleaned_data['password']
            url = 'http://127.0.0.1:8000/token-auth/'
            login_data = dict(username=input_username, password=input_password)
            response = requests.request("POST", url, data = login_data)
            request.session['token'] = "Token " +  str(response.json().get('token'))

            return HttpResponseRedirect('/todolists/')
    else:
        form = LoginForm()

    return render(request, 'login.tmpl', {'form': form})


def LogOut(request):
    try:
        del request.session['token']
    except KeyError:
        pass
    return HttpResponseRedirect('/login/')


def All_lists(request):
    try:
        req = requests.request("GET", 'http://127.0.0.1:8000/todolists/', headers={ 
            'Authorization': request.session['token']})

        tasklists = [tasklist for tasklist in json.loads(req.text)]
        template = get_template('lists.tmpl')
        context = {'tasklists': tasklists, 'Button_Create': True}
        return HttpResponse(template.render(context))
    except KeyError:
        return HttpResponseRedirect('/login/')


def Tasks(request,pk):
    try:
        req = requests.request("GET", 'http://127.0.0.1:8000/todolists/{pk}/tasks/'.format(pk=pk), headers={ 
            'Authorization': request.session['token']})
        tasks = [task for task in json.loads(req.text)]
        template = get_template('tasks.tmpl')
        try:
            context = {'tasks': tasks, 'list_id':pk, 'Button_Create': True}
        except:
            context={}
        return HttpResponse(template.render(context))
    except KeyError:
        return HttpResponseRedirect('/login/')


def CreateList(request):
    try:
        c = requests.Session()
        c.headers['Authorization'] = request.session['token']
    except KeyError:
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            url = 'http://127.0.0.1:8000/todolists/'
            data = form.cleaned_data
            p = c.post(url, data=data)
            return HttpResponseRedirect('/todolists/')
    else:
        form = ListForm()
    return render(request, 'list_create.tmpl', {'form': form})


def CreateTask(request,pk):

    try:
        c = requests.Session()
        c.headers['Authorization'] = request.session['token']
    except KeyError:
        return HttpResponseRedirect('/login/')
    url = 'http://127.0.0.1:8000/todolists/{pk}/tasks/'.format(pk=pk)
    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            c.post(url, data=form.cleaned_data)
            return HttpResponseRedirect('/todolists/{pk}/'.format(pk=pk))
    else:
        form = TaskCreateForm()

    return render(request, 'list_create.tmpl', {'form': form})


def ListEdit(request, list_id):
    try:
        c = requests.Session()
        c.headers['Authorization'] = request.session['token']
    except KeyError:
        return HttpResponseRedirect('/login/')

    url = 'http://127.0.0.1:8000/todolists/{list_id}/'.format(list_id=list_id)
    g = c.get(url)
    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            c.put(url, data=form.cleaned_data)
            return HttpResponseRedirect('/todolists/')
    else:
        form = ListForm(g.json())

    return render(request, 'list_create.tmpl', {'form': form})

def TaskEdit(request, list_id, pk):
    try:
        c = requests.Session()
        c.headers['Authorization'] = request.session['token']
    except KeyError:
        return HttpResponseRedirect('/login/')

    url = 'http://127.0.0.1:8000/todolists/{list_id}/tasks/{pk}/'.format(list_id=list_id, pk=pk)
    g = c.get(url)
    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            c.put(url, data=form.cleaned_data)
            return HttpResponseRedirect('/todolists/{list_id}/'.format(list_id=list_id))
    else:
        form = TaskCreateForm(g.json())

    return render(request, 'list_create.tmpl', {'form': form})


def TaskDelete(request,list_id, pk):
    try:
        c = requests.Session()
        c.headers['Authorization'] = request.session['token']
    except KeyError:
        return HttpResponseRedirect('/login/')
    url = 'http://127.0.0.1:8000/todolists/{list_id}/tasks/{pk}/'.format(list_id=list_id, pk=pk)
    c.delete(url)
    return HttpResponseRedirect('/todolists/{list_id}/'.format(list_id=list_id))


def ListDelete(request,list_id):
    try:
        c = requests.Session()
        c.headers['Authorization'] = request.session['token']
    except KeyError:
        return HttpResponseRedirect('/login/')
    url = 'http://127.0.0.1:8000/todolists/{list_id}/'.format(list_id=list_id)
    c.delete(url)
    return HttpResponseRedirect('/todolists/')


def ToShare(request,list_id):
    try:
        c = requests.Session()
        c.headers['Authorization'] = request.session['token']
    except KeyError:
        return HttpResponseRedirect('/login/')
    url = 'http://127.0.0.1:8000/todolists/{list_id}/share/'.format(list_id=list_id)

    if request.method == 'POST':
        form = ShareForm(request.POST)
        if form.is_valid():
            c.post(url, data=form.cleaned_data)
            return HttpResponseRedirect('/todolists/')

    else:
        form = ShareForm()

    return render(request, 'share.tmpl', {'form': form})


def SharedListView(request):
    try:
        req = requests.request("GET", 'http://127.0.0.1:8000/todolists/shared/', headers={ 
            'Authorization': request.session['token']})
        #print(req.json())
        tasklists = [tasklist for tasklist in json.loads(req.text)]
        template = get_template('lists.tmpl')
        context = {'tasklists': tasklists, 'Button_Create': False}
        return HttpResponse(template.render(context))
    except KeyError:
        return HttpResponseRedirect('/login/')


def SharedTasksView(request, list_id):
    try:
        req = requests.request("GET", 'http://127.0.0.1:8000/todolists/shared/{list_id}/'.format(list_id=list_id), headers={ 
            'Authorization': request.session['token']})
        tasks = [task for task in json.loads(req.text)]
        template = get_template('tasks.tmpl')
        context = {'tasks': tasks, 'Button_Create': False}
        return HttpResponse(template.render(context))
    except KeyError:
        return HttpResponseRedirect('/login/')


def Registration(request):
    c = requests.Session()
    c.headers['Authorization'] = 'Token a495bf7c7076bb4d2263b43e0e6f710ac0cdb175'
    url = 'http://127.0.0.1:8000/sign_up/'
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            c.post(url, data=form.cleaned_data)
            return HttpResponseRedirect('/todolists/')
    else:
        form = SignUpForm()

    return render(request, 'registration.tmpl', {'form': form})

    
