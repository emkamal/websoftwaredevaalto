from django.db import models

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
    name = model.CharField(max_length=50)
    email = model.EmailField()
    password = model.CharField(max_length=512)
    bio = model.TextField()
    register_date = models.DateTimeField()
    last_login = models.DateTimeField()
    user_type = model.CharField(max_length=10) # player, developer, admin
    is_validated = model.BooleanField()

class Game(models.Model):
    owner_id = models.ForeignKey(User)
    title = model.CharField(max_length=100)
    desc = model.TextField()
    instruction = model.TextField()
    url = model.URLField()
    price = model.FloatField()
