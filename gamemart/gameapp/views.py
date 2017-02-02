from django.http import HttpResponse, Http404
from django.shortcuts import render
from gameapp.forms import UserForm,SubmitForm


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
    return render(request, 'browse.html')

def submit(request):
    form = SubmitForm(request.POST or None)
    if form.is_valid():
        form.save()
    template = "submit.html"

    return render(request, template)

def gameview(request, id):
    return render(request, 'gameview.html')
