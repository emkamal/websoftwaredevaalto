from django.db import models
from django.contrib.auth.models import User

class Taxonomy(models.Model):
    taxonomy_type = models.CharField(max_length=20)
    label = models.CharField(max_length=50)
    parent_id = models.ForeignKey('self')

class Game_Taxonomy(models.Model):
    game_id = models.ForeignKey('Game')
    taxonomy_id = models.ForeignKey('Taxonomy')

class Review(models.Model):
    game_id = models.ForeignKey('Game')
    person_id = models.ForeignKey('Person')
    rating = models.IntegerField()
    review = models.TextField()

""" We extend User model which has the following fields:
-username
-email
-password
-last_login
That's why we don't have to write those fields to Person model"""
class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pic = models.ForeignKey('Asset', on_delete=models.CASCADE, related_name='assets')
    """name = models.CharField(max_length=50)"""
    """email = models.EmailField()"""
    """password = models.CharField(max_length=512)"""
    bio = models.TextField()
    register_date = models.DateTimeField()
    """last_login = models.DateTimeField()"""
    user_type = models.CharField(max_length=10) # player, developer, admin
    is_validated = models.BooleanField()

class Game(models.Model):
    owner_id = models.ForeignKey('Person')
    title = models.CharField(max_length=100)
    desc = models.TextField()
    instruction = models.TextField()
    url = models.URLField()
    price = models.FloatField()

class Asset(models.Model):
    asset_id = models.ForeignKey('Person')
    asset_type = models.CharField(max_length=50)
    url = models.URLField()
    owner_id = models.ForeignKey('Game')

class Gameplay(models.Model):
    player_id = models.ForeignKey('Person')
    game_id = models.ForeignKey('Game')
    score = models.FloatField()
    state = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now=True)

class Purchase(models.Model):
    buyer_id = models.ForeignKey('Person')
    game_id = models.ForeignKey('Game')
    date = models.DateTimeField(auto_now=True)
    amount = models.FloatField()
