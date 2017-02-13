from gameapp.models import *
from django.conf import settings

def load_taxonomies(request):
    game_categories = Taxonomy.objects.filter(taxonomy_type='game_category')
    game_tags = Taxonomy.objects.filter(taxonomy_type='game_tag')
    return {'game_categories': game_categories, 'game_tags': game_tags}

def load_state(request):
    userIsLoggedIn = False
    if request.user.is_authenticated():
        userIsLoggedIn = True

    return {
        'userIsLoggedIn': userIsLoggedIn
    }

def load_config(request):
    return {'BASE_URL': settings.BASE_URL}

# def load_taxonomy(type='game_category', num=3):
#     try:
#         taxonomies = {}
#         if mode == "all":
#             taxonomies_querysets = Taxonomy.objects.all()
#         elif mode == "game_category":
#             taxonomies_querysets = Taxonomy.objects.filter(type=type)[:num]
#         elif mode == "game_tag":
#             taxonomies_querysets = Taxonomy.objects.all()[:num]
#
#         # for game in games_querysets:
#         #
#         #     game_banner_url = 'http://192.168.5.5/media/site/no-image-400x250.jpg';
#         #     for asset in game.asset_set.all():
#         #         if asset.asset_type == 'game-banner-400x250':
#         #             game_banner_url = asset.url
#         #             break
#         #
#         #     games[game.id] = { 'title': game.title, 'price': game.price, 'desc': game.desc, 'slug': game.slug, 'banner_url': game_banner_url }
#
#         return taxonomies_querysets
#
#     except Game.DoesNotExist:
#         raise Http404("Game does not exist")
