from django.db import models
from django.contrib.auth.models import AbstractUser

class Taxonomy(models.Model):
    taxonomy_type = models.CharField(max_length=20)
    label = models.CharField(max_length=50)
    parent = models.ForeignKey('self')

class Game_Taxonomy(models.Model):
    game = models.ForeignKey('Game')
    taxonomy = models.ForeignKey('Taxonomy')

class Review(models.Model):
    game = models.ForeignKey('Game')
    person = models.ForeignKey('User')
    rating = models.IntegerField()
    review = models.TextField()

#class User(models.Model):
class User(AbstractUser):
    slug = models.CharField(max_length=100)
    pic = models.ForeignKey('Asset')
    bio = models.TextField()
    register_date = models.DateTimeField()
    #user_type values are player, developer and admin
    user_type = models.CharField(max_length=10)
    is_validated = models.BooleanField(default=False)

class Game(models.Model):
    owner = models.ForeignKey('User')
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    desc = models.TextField()
    instruction = models.TextField(blank=True)
    url = models.URLField()
    price = models.FloatField()
    added_date = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)


class Asset(models.Model):
    asset_type = models.CharField(max_length=50)
    url = models.URLField()
    # user = models.ForeignKey('User', null=True)
    game = models.ForeignKey('Game', null=True, on_delete=models.CASCADE)

class Gameplay(models.Model):
    player_id = models.ForeignKey('User')
    game_id = models.ForeignKey('Game')
    score = models.FloatField(default=0)
    state = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now=True)

class Purchase(models.Model):
    buyer_id = models.ForeignKey('User')
    game_id = models.ForeignKey('Game')
    date = models.DateTimeField(auto_now=True)
    amount = models.FloatField()
