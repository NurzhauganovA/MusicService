from django.utils import timezone

from django.db import models
from django.urls import reverse

from accounts.models import ArtistProfile, CustomUser
from music.helpers import get_audio_length
from music.validators import validate_is_audio

now = timezone.now()

class Genre(models.Model):
    name_of_genre = models.CharField(max_length=100, verbose_name='Genre name')
    description = models.TextField(verbose_name='Description of genre')

    def __str__(self):
        return str(self.name_of_genre)

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Music(models.Model):
    music_file = models.FileField(upload_to='musics/', verbose_name='Music File', validators=[validate_is_audio])
    cover_image = models.ImageField(upload_to='music_images/')
    name_of_song = models.CharField(max_length=250, verbose_name='Music name')
    author_name = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE, verbose_name='Select a author',
                                    related_name='authors', blank=True)
    genre = models.ManyToManyField(Genre, verbose_name='Genre of music')
    time_length = models.DecimalField(blank=True, max_digits=20, decimal_places=2)
    release_date = models.DateField(verbose_name='Release date', auto_now_add=True)
    text_of_song = models.TextField(verbose_name='Text of song', blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    like_music = models.ManyToManyField(CustomUser, verbose_name='Do you like this music?', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('detail_music', kwargs={'pk': self.id})

    def __str__(self):
        return str(self.name_of_song)

    class Meta:
        verbose_name = 'Music'
        verbose_name_plural = 'Musics'

    def save(self, *args, **kwargs):
        if not self.time_length:
            audio_length = get_audio_length(self.music_file)
            self.time_length = audio_length
        return super().save(*args, **kwargs)


class Album(models.Model):
    img = models.ImageField(upload_to='album_images/', verbose_name='Album Image')
    name_of_album = models.CharField(max_length=250, verbose_name='Album name')
    author_of_album = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE, verbose_name='Author of album',
                                        blank=True, null=True, related_name='my_albums')
    add_music = models.ManyToManyField(Music, verbose_name='Add music')
    date = models.DateField(verbose_name='Date', auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    like_album = models.ManyToManyField(CustomUser, verbose_name='Do you like this album?', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('detail_album', kwargs={'pk': self.id})

    def artist_detail(self):
        return self.author_of_album.id

    def __str__(self):
        return f"{str(self.name_of_album)} - {str(self.date)}"

    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'


