from django.http import HttpResponse, Http404
from django.shortcuts import render
from gameapp.forms import UserForm
from gameapp.models import *


def home(request):
    return render(request, 'home.html')
    # return HttpResponse('home_page')

def login(request):
    # return render(request, 'home.html')
    return HttpResponse('login_page')

def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.user_type = 'player'
            user.save()
            return redirect('home_page')
    else:
        user_form = UserForm()
    return render(request, 'registration/register.html', {'form': user_form })

def browse(request):

    try:
        games = Game.objects.all()
    except Game.DoesNotExist:
        raise Http404("Game does not exist")

    r = render (request, 'browse.html', {'games': games}, content_type='application/xhtml+xml')

    return HttpResponse(r)

    # return render(request, 'browse.html')

def submit(request):

    return render(request, 'submit.html')

def gameview(request, id):
    return render(request, 'gameview.html')
