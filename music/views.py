import cx_Oracle

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from music.forms import CreateMusicForm
from music.models import *


from django.views.generic import DetailView

@login_required
def index(request):

    userpswrd = "pswd"
    connection = cx_Oracle.connect(user="djangousr", password=userpswrd,
                                   dsn="localhost/orclpdb",
                                   encoding="UTF-8")

    cursor = connection.cursor()
    out_val = cursor.var(str)
    cursor.callproc('hello_time', [out_val])
    message = out_val.getvalue()
    cursor.close()

    cursor = connection.cursor()
    cursor.callproc('sorted_albums', [1])
    for implicit_cursor in cursor.getimplicitresults():
        sorted_albums = implicit_cursor.fetchall()
        sorted_album = sorted_albums[:5]
    cursor.close()


    all_music = Music.objects.all()
    all_albums = Album.objects.all()

   # sorted_album = all_albums.order_by('-date')[:5]
   # print(sorted_album)
    album_hiphop = set(all_albums.filter(add_music__genre__name_of_genre__exact='Hip-Hop'))
    album_rnb = set(all_albums.filter(add_music__genre__name_of_genre__exact='RnB'))

    context = {
        'all_music': all_music,
        'all_albums': all_albums,
        'sorted_album': sorted_album,
        'album_hiphop': album_hiphop,
        'album_rb': album_rnb,
        'message': message
    }

    return render(request, 'music/home.html', context)


class AlbumDetailView(DetailView):
    model = Album
    template_name = 'music/album_detail.html'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        all_music = Music.objects.filter()
        context = super(AlbumDetailView, self).get_context_data(**kwargs)
        stuff = get_object_or_404(Album, id=self.kwargs['pk'])

        liked_album = False
        if stuff.like_album.filter(id=self.request.user.id).exists():
            liked_album = True

        context['liked_album'] = liked_album

        liked_music = False
        if stuff.add_music.filter(like_music__id=self.request.user.id).exists():
            liked_music = True

        context['liked_music'] = liked_music

        every_liked_music = []
        its_id = self.request.user.id
        userpswrd = "pswd"
        connection = cx_Oracle.connect(user="djangousr", password=userpswrd,
                                       dsn="localhost/orclpdb",
                                       encoding="UTF-8")
        cursor = connection.cursor()
        cursor.callproc('liked_musics', [its_id])
        for implicit_cursor in cursor.getimplicitresults():
            for row in implicit_cursor:
                every_liked_music.append(row)

        check_liked = False
        checks_liked = []
        for al in Album.objects.filter(add_music__id__exact=self.object.id):
            for mus in al.add_music.all():
                for ery_liked_music in every_liked_music:
                    if ery_liked_music[0] == mus.id:
                        check_liked=True
                        break
                    else:
                        check_liked=False
                if check_liked:
                    checks_liked.append(True)
                else:
                    checks_liked.append(False)

        context['checks_liked'] = checks_liked


        return context


class ArtistDetailView(DetailView):
    model = ArtistProfile
    template_name = 'music/artist_detail.html'
    context_object_name = 'artist'

    def get_context_data(self, **kwargs):
        context = super(ArtistDetailView, self).get_context_data(**kwargs)
        genre_music = Music.objects.all()
        genre_album = Album.objects.all()
        genre_music_list = genre_music.filter(genre__music__author_name__exact=self.object.id)
        genre_album_list = genre_album.filter(add_music__genre__music__author_name__exact=self.object.id)
        context['music_list'] = Music.objects.filter(author_name__user__username__exact=self.object.user.username)
        context['album_list'] = set(Album.objects.filter(author_of_album__user__username__exact=self.object.user.username))
        context['similar_musics'] = set(genre_music_list.order_by()[:5])
        context['similar_albums'] = set(genre_album_list)

        userpswrd = "pswd"
        connection = cx_Oracle.connect(user="djangousr", password=userpswrd,
                                       dsn="localhost/orclpdb",
                                       encoding="UTF-8")
        cursor = connection.cursor()

        artist_id = get_object_or_404(ArtistProfile, id=self.kwargs['pk']).id
        return_val = cursor.callfunc('sum_likes', int, [artist_id])
        context['sum_likes_of_artist'] = return_val

        return context


class MusicDetailView(DetailView):
    model = Music
    template_name = 'music/music_detail.html'
    context_object_name = 'music'

    def get_context_data(self, **kwargs):
        context = super(MusicDetailView, self).get_context_data(**kwargs)
        context['lyric_music'] = (Music.text_of_song, '.txt')
        context['music_list'] = Music.objects.filter(id__exact=self.object.id)
        return context


class GenreDetailView(DetailView):
    model = Genre
    template_name = 'music/genre_detail.html'
    context_object_name = 'genre'

    def get_context_data(self, **kwargs):
        context = super(GenreDetailView, self).get_context_data(**kwargs)
        context['genre_list'] = Music.objects.filter(genre__exact=self.object.id)
        return context


def search(request):
    all_genres = Genre.objects.all().order_by()[:5]
    all_artists = ArtistProfile.objects.all()

    context = {
        'all_genres': all_genres,
        'all_artists': all_artists

    }

    return render(request, 'music/search.html', context)

def LikeAlbum(request, pk):
    album_like = get_object_or_404(Album, id=request.POST.get('album_id'))
    liked_album = False
    if album_like.like_album.filter(id=request.user.id).exists():
        album_like.like_album.remove(request.user)
        liked_album = False
    else:
        album_like.like_album.add(request.user)
        liked_album = True
    return HttpResponseRedirect(reverse('detail_album', args=[str(pk)]))


def LikeMusic(request, pk):
    music_like = get_object_or_404(Music, id=request.POST.get('music_id'))
    liked_music = False
    if music_like.like_music.filter(id=request.user.id).exists():
        music_like.like_music.remove(request.user)
        liked_music = False
    else:
        music_like.like_music.add(request.user)
        liked_music = True
    return HttpResponseRedirect(reverse('detail_album', args=[str(pk)]))


def FavoriteMusics(request):
    all_musics = Music.objects.all()
    like_musics = Music.objects.filter(like_music__id=request.user.id)

    context = {
        'like_musics': like_musics,
        'all_musics': all_musics,
    }

    return render(request, 'music/favorite_musics.html', context)


def FavoriteAlbums(request):
    all_albums = Album.objects.all()
    like_albums = Album.objects.filter(like_album__id=request.user.id)

    context = {
        'like_albums': like_albums,
        'all_albums': all_albums,
    }

    return render(request, 'music/favorite_albums.html', context)


def AllGenres(request):
    all_genres = Genre.objects.all()

    context = {
        'all_genres': all_genres
    }

    return render(request, 'music/all_genres.html', context)


def AllArtists(request):
    all_artists = ArtistProfile.objects.all()

    context = {
        'all_artists': all_artists
    }

    return render(request, 'music/all_artists.html', context)


def AcceptCreated(request):
    return render(request, 'music/accept_created.html')


def CreateMusic(request):
    error = ''
    if request.method == 'POST':
        form = CreateMusicForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = request.user
            artist = ArtistProfile.objects.get(user=user_id)
            form.instance.author_name = artist
            form.save()
            return redirect('accept_created')
        else:
            error = 'The Form was incorrect!'

    form = CreateMusicForm(request.POST, request.FILES)

    context = {
        'form': form,
        'error': error
    }

    return render(request, 'music/create_music.html', context)
