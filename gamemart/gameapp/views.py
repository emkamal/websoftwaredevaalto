
from django.http import HttpResponse, Http404
from django.shortcuts import render
"""from gameapp.models import Product"""

def login(request):
    return render(request, "register/login.html")

def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            return redirect('home_page')
    else:
        user_form = UserForm()
    return render(request, 'registration/register.html', {'form': user_form })
