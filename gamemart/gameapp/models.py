from django.db import models
from django.contrib.auth.models import AbstractUser

class Taxonomy(models.Model):
    taxonomy_type = models.CharField(max_length=20)
    label = models.CharField(max_length=50)
    parent_id = models.ForeignKey('self')

class Game_Taxonomy(models.Model):
    game_id = models.ForeignKey('Game')
    taxonomy_id = models.ForeignKey('Taxonomy')

class Review(models.Model):
    game_id = models.ForeignKey('Game')
    person_id = models.ForeignKey('User')
    rating = models.IntegerField()
    review = models.TextField()

#class User(models.Model):
class User(AbstractUser):
    pic = models.ForeignKey('Asset', on_delete=models.CASCADE, related_name='assets')
    bio = models.TextField()
    register_date = models.DateTimeField()
    #user_type values are player, developer and admin
    user_type = models.CharField(max_length=10)
    is_validated = models.BooleanField()

class Game(models.Model):
    owner_id = models.ForeignKey('User')
    title = models.CharField(max_length=100)
    desc = models.TextField()
    instruction = models.TextField()
    url = models.URLField()
    price = models.FloatField()

class Asset(models.Model):
    asset_id = models.ForeignKey('User')
    asset_type = models.CharField(max_length=50)
    url = models.URLField()
    owner_id = models.ForeignKey('Game')

class Gameplay(models.Model):
    player_id = models.ForeignKey('User')
    game_id = models.ForeignKey('Game')
    score = models.FloatField()
    state = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now=True)

class Purchase(models.Model):
    buyer_id = models.ForeignKey('User')
    game_id = models.ForeignKey('Game')
    date = models.DateTimeField(auto_now=True)
    amount = models.FloatField()
