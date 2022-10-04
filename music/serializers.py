from music.models import FavouriteAlbum


class UserFavouriteAlbumSerializer(ModelSerializer):
    class Meta:
        model = FavouriteAlbum
        fields = ('album_id', 'fav_album')
