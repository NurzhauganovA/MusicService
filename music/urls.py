from django.urls import path
from . import views


urlpatterns = [
    path('browse', views.index, name='browse_music'),
    path('album/<int:pk>', views.AlbumDetailView.as_view(), name='detail_album'),
    path('artist/<int:pk>', views.ArtistDetailView.as_view(), name='detail_artist'),
    path('search', views.search, name='search'),
    path('<int:pk>', views.MusicDetailView.as_view(), name='detail_music'),
    path('genre/<int:pk>', views.GenreDetailView.as_view(), name='detail_genre'),
    path('like_album/<int:pk>', views.LikeAlbum, name='like_album'),
    path('like_music/<int:pk>', views.LikeMusic, name='like_music'),
    path('favorite_albums', views.FavoriteAlbums, name='favorite_albums'),
    path('favorite_musics', views.FavoriteMusics, name='favorite_musics'),
    path('all_genres', views.AllGenres, name='all_genres'),
    path('all_artists', views.AllArtists, name='all_artists'),
    path('create_music', views.CreateMusic, name='create_music'),
    path('accept_created', views.AcceptCreated, name='accept_created'),

]
