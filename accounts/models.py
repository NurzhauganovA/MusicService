from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    authorcheck = models.BooleanField(default=False)
    premiumcheck = models.BooleanField(default=False)


class ArtistProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    artist_name = models.CharField(max_length=250, verbose_name='Artist name')
    artist_img = models.ImageField(upload_to='artist_images/')
    artist_poster_img = models.ImageField(upload_to='artist_poster_images/')
    birthdate = models.DateField()
    country = models.CharField(max_length=250, verbose_name='Country')


    def __str__(self):
        return str(self.artist_name)

    class Meta:
        verbose_name = 'Artist'
        verbose_name_plural = 'Artists'
