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
