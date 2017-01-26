from django.http import HttpResponse, Http404
from django.shortcuts import render
from gameapp.forms import UserForm


def home(request):
    #return render(request, 'home.html')
    return HttpResponse('home_page')

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
