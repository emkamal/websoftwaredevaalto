from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from gameapp.forms import UserForm
#from gameapp import views

def home(request):
    return render(request, 'home.html')
    # return HttpResponse('home_page')

def login(request):
    # return render(request, 'home.html')
    # return HttpResponse('login_page')
    return render(request, 'home.html', {})
    #return HttpResponse('home_page')

def registration(request):
    return render(request, 'register.html', {})

def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.user_type = 'player'
            user.save()
            return render(request, 'debug.html', {'user': user})    #this is for testing
            #return redirect('home_page')
    else:
        user_form = UserForm()
    return render(request, 'register.html', {'form': user_form })

def browse(request):
    return render(request, 'browse.html')

def submit(request):
    return render(request, 'submit.html')

def gameview(request, id):
    return render(request, 'gameview.html')
