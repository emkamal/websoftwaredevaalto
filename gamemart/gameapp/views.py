from django.http import HttpResponse, Http404
from django.shortcuts import *
from gameapp.forms import UserForm, SubmitForm
from gameapp.models import *
from django.conf import settings
from hashlib import md5


def home(request):
    featured_games = load_games('featured', '', 3)
    latest_games = load_games('latest', '', 4)
    r = render (
        request,
        'home.html',
        {
            'page_title': 'Javascript Game Marketplace',
            'page_subtitle': 'Sell your games here and let others play',
            'featured_games': featured_games,
            'latest_games': latest_games
        },
        content_type='application/xhtml+xml'
    )

    return HttpResponse(r)
    # return HttpResponse('home_page')

def login(request):
    # return render(request, 'home.html')
    # return HttpResponse('login_page')
    return render(request, 'home.html', {})
    #return HttpResponse('home_page')

def registration(request):
    return render(request, 'register.html', {})

def registrationDeveloper(request):
    return render(request, 'registerDeveloper.html', {})

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
    return render(request, 'register.html', {'form': user_form })

def browse(request):
    games = load_games(request, 'featured')

    r = render (
        request,
        'browse.html',
        {
            'page_title': 'Games collection',
            'page_subtitle': 'Explore our game collection',
            'games': games
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

def explore_by_taxonomy(request, tag):
    # taxonomy_type = request.path.split('/')[2]
    target = Taxonomy.objects.get(slug=tag)
    page_title = target.label
    tag_id = target.id

    # games_exist = True
    games = load_games('tag', tag_id)

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
        games = {}
        if mode == "all":
            games_querysets = Game.objects.all()
        elif mode == "featured":
            games_querysets = Game.objects.filter(is_featured=True)[:num]
        elif mode == "latest":
            games_querysets = Game.objects.all()[:num]
        elif mode == "tag":
            games_querysets = Game.objects.filter(game_taxonomy=tags)

        for game in games_querysets:

            game_banner_url = 'http://192.168.5.5/media/site/no-image-400x250.jpg';
            for asset in game.asset_set.all():
                if asset.asset_type == 'game-banner-400x250':
                    game_banner_url = asset.url
                    break

            if game.id in user_owner_games:
                game_bought = True
            else:
                game_bought = False

            games[game.id] = {
                'id': game.id,
                'title': game.title,
                'price': game.price,
                'desc': game.desc,
                'slug': game.slug,
                'banner_url': game_banner_url,
                'bought': game_bought,
                'a': user_owner_games
            }

        return games

    except Game.DoesNotExist:
        raise Http404("Game does not exist")

def submit(request):
    form = SubmitForm(request.POST or None)
    if form.is_valid():
        form.save()

    return render(request, 'submit.html')

def game_by_id(request, id):
    game = get_object_or_404(Game, id=id)

    purchase = Purchase.objects.latest('id')
    next_purchase_id = purchase.id+1;

    checksumstr = "pid={}&sid={}&amount={}&token={}".format(next_purchase_id, SELLER_ID, game.price, PAYMENT_SECRET_KEY)
    checksum = md5(checksumstr.encode("ascii")).hexdigest()

    return render(request, 'gameview.html', {'game': game, 'next_purchase_id': next_purchase_id, 'page_title': game.title, 'checksum': checksum})

def game_by_slug(request, slug):
    game = get_object_or_404(Game, slug=slug)

    game_bought = False

    if(request.user.is_authenticated()):
        user_purchases = Purchase.objects.filter(buyer_id=request.user.id)
        if user_purchases.exists():
            for user_purchase in user_purchases:
                if user_purchase.game_id == game.id and user_purchase.state == 'success' :
                    game_bought = True

    purchase = Purchase.objects.latest('id')
    next_purchase_id = purchase.id+1;

    checksumstr = "pid={}&sid={}&amount={}&token={}".format(next_purchase_id, settings.SELLER_ID, game.price, settings.PAYMENT_SECRET_KEY)
    checksum = md5(checksumstr.encode("ascii")).hexdigest()

    return render(request, 'gameview.html', {'game': game, 'next_purchase_id': next_purchase_id, 'page_title': game.title, 'checksum': checksum, 'game_bought': game_bought})

def payment(request, status, slug):
    game = get_object_or_404(Game, slug=slug)
    purchase = Purchase(amount=game.price, buyer_id=request.user.id, game_id=game.id, status=status)
    purchase.save()

    return render(request, 'payment.html', {'status': status})
