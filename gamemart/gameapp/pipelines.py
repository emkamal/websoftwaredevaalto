import itertools

from gameapp.models import User
from django.utils.text import slugify

def create_slug(backend, user, response, *args, **kwargs):
    if backend.name == 'github':
        username = response.get('login')
    elif backend.name == 'twitter':
        username = response.get('screen_name')

    user.slug = orig = slugify(username)

    for x in itertools.count(1):
        if not User.objects.filter(slug=user.slug).exists():
            break
        user.slug = '%s-%d' % (orig, x)

    user.save()
