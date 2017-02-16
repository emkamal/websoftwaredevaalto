from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField

class Taxonomy(models.Model):
    taxonomy_type = models.CharField(max_length=20)
    label = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    parent = models.ForeignKey('self',null=True,blank=True)
    # games = models.ManyToManyField('Game')

    def __str__(self):
        return u'%s' % (self.label)

# class Game_Taxonomy(models.Model):
#     game = models.ForeignKey('Game')
#     taxonomy = models.ForeignKey('Taxonomy')

class Review(models.Model):
    game = models.ForeignKey('Game')
    person = models.ForeignKey('User')
    rating = models.IntegerField()
    review = models.TextField()

    def __str__(self):
        return u'review by %s on %s' % (self.person, self.game)

#class User(models.Model):
class User(AbstractUser):
    slug = models.SlugField(max_length=100, unique=True)
    pic = models.ForeignKey('Asset', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    register_date = models.DateTimeField(auto_now=True,null=True, blank=True)
    #user_type values are player, developer and admin
    user_type = models.CharField(max_length=10,default='player')
    is_validated = models.BooleanField(default=False)

    def __str__(self):
        return u'%s %s' % (self.first_name, self.last_name)

class Game(models.Model):
    owner = models.ForeignKey('User')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    desc = models.TextField(blank=True)
    instruction = models.TextField(blank=True)
    url = models.URLField()
    price = models.FloatField()
    added_date = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    taxonomies = models.ManyToManyField('Taxonomy')
    # banner = model.ImageField(upload_to='games')

    def __str__(self):
        return u'%s' % (self.title)

class Asset(models.Model):
    asset_type = models.CharField(max_length=50)
    url = models.FileField()
    # user = models.ForeignKey('User', null=True)
    game = models.ForeignKey('Game', null=True, on_delete=models.CASCADE)

class Gameplay(models.Model):
    player = models.ForeignKey('User', on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    score = models.FloatField(default=0, null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

class Purchase(models.Model):
    buyer = models.ForeignKey('User', on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    amount = models.FloatField()
    status = models.CharField(max_length=50, default='error')
