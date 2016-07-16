from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class GameLibrary(models.Model):
    '''
    Just contains a reference to which games are uploaded and some info about them
    '''
    name = models.CharField(max_length=36)
    thumbnail = models.ImageField(upload_to='thumbnails')#will it be easier to add games via admin as opposed to manually. esp when in production
    description = models.CharField(max_length=256)
    creation_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    '''
    Contains profile data for registered users.
    '''
    user = models.OneToOneField(User, related_name='profile')
    nickname = models.CharField(max_length=20)
    played_games = models.ManyToManyField(GameLibrary)

    def __str__(self):
        return self.nickname
