from django.contrib import admin
from music.models import *

admin.site.register(Genre)


class MusicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name_of_song',)}


class AlbumAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name_of_album',)}


admin.site.register(Music, MusicAdmin)
admin.site.register(Album, AlbumAdmin)
