from django.http import HttpResponse, Http404
from django.shortcuts import *
# from gameapp.forms import UserForm, SubmitForm
from gameapp.models import *


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
    try:
        games = Game.objects.all()
    except Game.DoesNotExist:
        raise Http404("Game does not exist")

    r = render (request, 'browse.html', {'games': games}, content_type='application/xhtml+xml')

    return HttpResponse(r)

    # return render(request, 'browse.html')

def submit(request):
    form = SubmitForm(request.POST or None)
    if form.is_valid():
        form.save()

    return render(request, 'submit.html')

def game_by_id(request, id):
    game = get_object_or_404(Game, id=id)
    return render(request, 'gameview.html', {'game': game})

def game_by_slug(request, slug):
    game = get_object_or_404(Game, slug=slug)
    return render(request, 'gameview.html', {'game': game})
