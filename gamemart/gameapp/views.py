from django.http import HttpResponse, Http404
from django.shortcuts import *
from gameapp.forms import UserForm
from gameapp.models import *
from django.conf import settings
from hashlib import md5
from django.shortcuts import render
#from django.contrib.auth import authenticate, login
from .forms import SubmitForm
#from .forms import LoginForm, SubmitForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import redirect
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import operator
import os
import io
import sys
from PIL import Image, ImageOps

def home(request):
    featured_games = load_games(request, 'featured', '', 3)
    latest_games = load_games(request, 'latest', '', 6)
    r = render (
        request,
        'home.html',
        {
            'page_title': 'Javascript Game Marketplace',
            'page_subtitle': 'Sell your games here and let others play',
            'featured_games': featured_games,
            'latest_games': latest_games,
            'next_purchase_id': next_purchase_id(),
        },
        content_type='application/xhtml+xml'
    )

    return HttpResponse(r)

#def user_login(request):
#    if request.method == 'POST':
#        form =  LoginForm(request.POST)
#        if form.is_valid():
#            cd = form.cleaned_data
#            user = authenticate(username=cd['username'],
#                    password=cd['password'])
#            if user is not None:
#                if user.is_active:
#                    login(request, user)
#                    return HttpResponse('Authenticated '\
#                            'successfully')
#            else:
#                return HttpResponse('Disabled account')
#        else:
#            return HttpResponse('Invalid login')
#    else:
#        form = LoginForm()
#    return render(request, 'account/login.html', {'form':form})

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section':'dashboard'})


#def login(request):
    # return render(request, 'home.html')
    # return HttpResponse('login_page')
    #return render(request, 'home.html', {})
    #return HttpResponse('home_page')

def registration(request):
    return render(request, 'register.html', {'page_title': 'Registration'})

def registrationDeveloper(request):
    return render(request, 'registerDeveloper.html', {'page_title': 'Developer Registration'})

def registrationAdmin(request):
    return render(request, 'registerAdmin.html', {})

def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            #user.user_type = 'player'
            user.save()
            #return render(request, 'debug.html', {'user': user})    #this is for testing
            return redirect('login')
    else:
        user_form = UserForm()
    return render(request, 'register.html', {'form': user_form, 'page_title': 'Registration' })

def browse(request):
    games = load_games(request, 'featured')

    r = render (
        request,
        'browse.html',
        {
            'page_title': 'Games collection',
            'page_subtitle': 'Explore our game collection',
            'games': games,
            'next_purchase_id': next_purchase_id()
        },
        content_type='application/xhtml+xml'
    )

    return HttpResponse(r)

def explore(request, type):
    if type == 'featured':
        page_title = 'Featured'
        games = load_games(request, 'featured')
    elif type == 'latest':
        page_title = 'Latest'
        games = load_games(request)
    elif type == 'top-rated':
        page_title = 'Top Rated'
        games = load_games(request)
    elif type == 'top-grossing':
        page_title = 'Top Grossing'
        games = load_games(request)
    elif type == 'most-played':
        page_title = 'Most Played'
        games = load_games(request)
    else:
        raise Http404

    paginated_games = games_paginator(request, games, 9)

    r = render (
        request,
        'browse.html',
        {
            'page_title': page_title + " Games",
            'page_subtitle': '',
            'games': paginated_games,
            'next_purchase_id': next_purchase_id()
        },
        content_type='application/xhtml+xml'
    )

    return HttpResponse(r)

def games_paginator(request, games, num_per_page):
    paginator = Paginator(games, num_per_page)

    page = request.GET.get('page')

    try:
        paginated_games = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_games = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_games = paginator.page(paginator.num_pages)

    return paginated_games

def explore_by_taxonomy(request, tag):
    # taxonomy_type = request.path.split('/')[2]
    target = Taxonomy.objects.get(slug=tag)
    page_title = target.label
    tag_id = target.id

    # games_exist = True
    games = load_games(request, 'tag', tag_id)
    r = render (
        request,
        'browse.html',
        {
            'page_title': page_title + " Games",
            'page_subtitle': '',
            'games': games
        },
        content_type='application/xhtml+xml'
    )

    return HttpResponse(r)


def load_games(request, mode="all", tags="", num=3):
    # all, featured, latest, tags,

    user_owner_games = [];

    if(request.user.is_authenticated()):
        user_purchases = Purchase.objects.filter(buyer_id=request.user.id)
        if user_purchases.exists():
            for user_purchase in user_purchases:
                user_owner_games.append(user_purchase.game_id)

    try:
        games = []
        if mode == "all":
            games_querysets = Game.objects.all()
        elif mode == "featured":
            games_querysets = Game.objects.filter(is_featured=True)[:num]
        elif mode == "latest":
            games_querysets = Game.objects.all().order_by('-added_date')[:num]
        elif mode == "tag":
            games_querysets = Game.objects.filter(taxonomy=tags)

        games = build_games_view(request, games_querysets)

        return games

    except Game.DoesNotExist:
        raise Http404("Game does not exist")

def build_games_view(request, querysets):

    user_owned_games = [];

    if(request.user.is_authenticated()):
        user_purchases = Purchase.objects.filter(buyer_id=request.user.id)
        if user_purchases.exists():
            for user_purchase in user_purchases:
                user_owned_games.append(user_purchase.game_id)

    output = []

    for game in querysets:
        game_banner_url = 'http://192.168.5.5/media/site/no-image-400x250.jpg';
        for asset in game.asset_set.all():
            if asset.asset_type == 'game-banner-400x250':
                game_banner_url = asset.url
                break

        if game.id in user_owned_games:
            game_bought = True
        else:
            game_bought = False

        checksum = get_checksum(game.price)

        output.append({
            'id': game.id,
            'title': game.title,
            'price': game.price,
            'desc': game.desc,
            'slug': game.slug,
            'banner_url': game_banner_url,
            'bought': game_bought,
            'checksum': checksum
        })

    return output

def submit(request):
    if not request.user.is_authenticated:
        return redirect((settings.LOGIN_URL))
    if request.method == "POST":
        form = SubmitForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save(request)
            game.save()

            categories = form.cleaned_data['categories']

            for category in categories:
                game.taxonomies.add(category.id)

            handle_uploaded_file(request, request.FILES['image'], game)

            return redirect('home_page')
    else:
        form = SubmitForm()
    return render(request, 'submit.html', {'form': form, 'page_title': 'Submit Games'})

def handle_uploaded_file(request, file, game):
    # with open('/media/image.jpg', 'wb+') as destination:
    #     for chunk in file.chunks():
    #         destination.write(chunk)

    # folder = request.path.replace("/", "_")
    # folder = 'media/games/'
    folder = 'media/games/' + game.slug
    original_filename, original_fileext = os.path.splitext(request.FILES['image'].name)
    uploaded_filename = game.slug+"-banner-original-size"+original_fileext

    # create the folder if it doesn't exist.
    try:
        os.mkdir(os.path.join(settings.BASE_DIR, folder))
    except:
        pass

    # save the uploaded file inside that folder.
    full_filename = os.path.join(settings.BASE_DIR, folder, uploaded_filename)
    fout = io.open(full_filename, 'wb+')
    # Iterate through the chunks.
    for chunk in file.chunks():
        fout.write(chunk)
    fout.close()

    generate_thumbnails(full_filename, game)

def generate_thumbnails(filename, game):
    sizes = {
        '128x128': (128, 128),
        '400x250': (400, 250),
        '750x400': (750, 400)
    }

    for key, size in sizes.items():
        outfile = filename.replace('original-size', key)

        try:
            im = Image.open(filename)
            # im.thumbnail(size)
            # im.save(outfile, "JPEG")
            thumb = ImageOps.fit(im, size, Image.ANTIALIAS)
            thumb.save(outfile, "JPEG")

            asset = Asset(asset_type='game-banner-'+key,url=outfile.replace(settings.BASE_DIR, ''),game_id=game.id)
            asset.save()

        except IOError:
            print("cannot create thumbnail for")

def next_purchase_id():
    purchase = Purchase.objects.latest('id')
    next_purchase_id = int(purchase.id)+1;
    return next_purchase_id

def get_checksum(amount):
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(next_purchase_id(), settings.SELLER_ID, amount, settings.PAYMENT_SECRET_KEY)
    checksum = md5(checksumstr.encode("ascii")).hexdigest()
    return checksum

def game_by_slug(request, slug):
    game = get_object_or_404(Game, slug=slug)

    game_bought = False

    if(request.user.is_authenticated()):
        user_purchases = Purchase.objects.filter(buyer_id=request.user.id)
        if user_purchases.exists():
            for user_purchase in user_purchases:
                if user_purchase.game_id == game.id and user_purchase.status == 'success' :
                    game_bought = True


    gameplays = Gameplay.objects.filter(game_id=game.id).order_by('score')

    highscore = {}
    play_count = 0
    for gameplay in gameplays:
        play_count += 1
        if gameplay.score is not None:
            if gameplay.player_id in highscore:
                if gameplay.score > highscore[gameplay.player_id]:
                    highscore[gameplay.player_id] = gameplay.score
            else:
                highscore[gameplay.player_id] = gameplay.score

    highscore_output = {}
    for key, score in highscore.items():
        # user = get_object_or_404(User, id=int(key))
        user = User.objects.get(pk=int(key))
        highscore_output[user.username] = highscore[key]

    highscore_sorted = sorted(highscore_output.items(), key=operator.itemgetter(1), reverse=True)

    checksum = get_checksum(game.price)

    purchases = Purchase.objects.filter(game_id=game.id)

    game_banner_url = 'none';
    for asset in game.asset_set.all():
        if asset.asset_type == 'game-banner-750x400':
            game_banner_url = asset.url
            break

    return render(
        request,
        'gameview.html',
        {
            'game': game,
            'game_banner_url': game_banner_url,
            'next_purchase_id': next_purchase_id(),
            'page_title': game.title,
            'checksum': checksum,
            'game_bought': game_bought,
            'highscore': highscore_sorted,
            'play_count': play_count,
            'purchase_count': purchases.count()
        }
    )

def payment(request, status, slug):
    game = get_object_or_404(Game, slug=slug)
    purchase = Purchase(amount=game.price, buyer_id=request.user.id, game_id=game.id, status=status)
    purchase.save()

    return render(request, 'payment.html', {'status': status, 'game': game })

def api(request, target):
    output = {}

    if target == 'game':
        target_model = Game
    elif target == 'user':
        target_model = User
    elif target == 'gameplay':
        target_model = Gameplay
    else:
        return HttpResponse('{}', content_type="application/json")

    if request.method == 'GET':

        objects = target_model.objects.all();

        if target == 'gameplay' and request.GET.get("game_id") is not None:
            objects = objects.filter(game_id=request.GET.get("game_id"), player_id=request.user.id).latest('timestamp')

        try:
            _ = (e for e in objects)
        except TypeError:
            output = {
                'id': objects.id,
                'score': objects.score,
                'state': objects.state,
                'game_id': objects.game_id,
                'player_id': objects.player_id,
            }
        else:
            i = 0
            for obj in objects:
                if target == 'game':
                    output[i] = {
                        'id': obj.id,
                        'title': obj.title,
                        'price': obj.price,
                    }
                elif target == 'user':
                    output[i] = {
                        'id': obj.id,
                        'first_name': obj.first_name,
                        'last_name': obj.last_name,
                    }
                elif target == 'gameplay':
                    output[i] = {
                        'id': obj.id,
                        'score': obj.score,
                        'state': obj.state,
                        # 'timestamp': obj.timestamp,
                        'game_id': obj.game_id,
                        'player_id': obj.player_id,
                    }

                i = i+1

        json_dump = json.dumps(output)

        return HttpResponse(json_dump, content_type="application/json")

    elif request.method == 'POST':
        data = request.POST
        if target == 'gameplay':
            try:
                g = Gameplay(score=data.get('score'), state=data.get('state'), game_id=data.get('game_id'), player_id=request.user.id)
                g.save()
                return HttpResponse('success', content_type="application/json")
            except Gameplay.DoesNotExist:
                raise Http404("Gameplay does not exist")
            except Exception as e:
                return HttpResponse(e, content_type="application/json")

        else:
            return HttpResponse(target, content_type="application/json")

def search(request):
    if(request.GET.get("keywords") is None):
        keywords_string = ''
    else:
        keywords_string = request.GET.get("keywords")

    keywords = keywords_string.split(' ')
    objects_list = []
    output = Game.objects.none()

    for keyword in keywords:
        objects_list.append(Game.objects.filter(title__icontains=keyword))
        objects_list.append(Game.objects.filter(desc__icontains=keyword))

    for obj in objects_list:
        output = output | obj

    games = build_games_view(request, output)

    paginated_games = games_paginator(request, games, 9)

    return render(request, 'search.html', {'games': paginated_games, 'page_title': keywords_string + " games", 'search_string': 'keywords='+keywords_string })
