om django.db import models

class Taxonomy(models.Model):
    taxonomy_type = models.CharField(max_length=20)
    label = models.CharField(max_length=50)
    parent_id = models.ForeignKey('self')

class Game_Taxonomy(models.Model):
    game_id = models.ForeignKey(Game)
    taxonomy_id = models.ForeignKey(Taxonomy)

class Review(models.Model):
    game_id = models.ForeignKey(Game)
    user_id = models.ForeignKey(User)
    rating = models.IntegerField()
    review = models.TextField()

class User(models.Model):
    pic = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='assets')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=512)
    bio = models.TextField()
    register_date = models.DateTimeField()
    last_login = models.DateTimeField()
    user_type = models.CharField(max_length=10) # player, developer, admin
    is_validated = models.BooleanField()

class Game(models.Model):
    owner_id = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    desc = models.TextField()
    instruction = models.TextField()
    url = models.URLField()
    price = models.FloatField()

class Asset(models.Model):
    asset_id = models.ForeignKey(User)
    asset_type = models.CharField(max_length=50)
    url = models.URLField()
    owner_id models.ForeignKey(Game)

class Gameplay(models.Model):
    player_id = models.ForeignKey(User)
    game_id = models.ForeignKey(game)
    score = models.FloatField()
    state = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now=true)

class Purchase(models.Models):
    buyer_id = models.ForeignKey(User)
    game_id = models.ForeignKey(Game)
    date = models.DateTimeField(auto_now=true)
    amount = models.FloatField()
