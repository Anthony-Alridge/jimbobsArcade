from django.shortcuts import render
from .forms import LoginForm, RegistrationForm
from .models import GameLibrary, Profile
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
# Create your views here.

def game_canvas(request):
    '''
    finds related js file to retrieve game and provides a canvas to play game on.
    '''
    filename = request.get_full_path().split('/game_')[1]
    context= {'js_name':filename}
    return render(request, 'games/game.html', context)

def library(request):
    '''
    handles search requests for games. Lists games added to db most recently, or
    users most used if theyare signed in.
    '''
    if request.POST:
        query = request.POST.get('query')
        games = GameLibrary.objects.filter(name__contains=query)
        if not games:
            games = False
        #user is searching for a game. query db and return results.
    else:
        #user has navigated to this page.
        if request.user.is_authenticated():
            games = request.user.profile.played_games.all()
            if not games:
                games = GameLibrary.objects.order_by('creation_date')[0:3]#sort by date added, use first three.
        else:
            games = GameLibrary.objects.order_by('creation_date')[0:3]

    context = {'games': games}
    return render(request, 'games/library.html', context)

def signIn(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('games:library'))

            else:
                    form = LoginForm()
                    context = {'form':form}
                    return render(request, 'games/signIn.html', context)
    else:
        form = LoginForm()
        context = {'form': form}
        return render(request, 'games/signIn.html', context)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            nickname = form.cleaned_data['password']
            user = User.objects.create_user(username = username, password = password)
            user.save()
            p = Profile(user = user, nickname = nickname)
            p.save()
            return HttpResponseRedirect(reverse('games:library'))
        else:
            context = {'form': form}
            return render(request, 'games/register.html', context)

    else:
        form = RegistrationForm()
        context = {'form': form}
        return render(request, 'games/register.html', context)
