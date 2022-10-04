from django.urls import resolve


def message_processor(request):
    url_name = resolve(request.path_info).url_name

    if url_name == 'browse_music' or url_name == 'detail_album' or url_name == 'detail_artist' or url_name == 'search' \
            or url_name == 'detail_music' or url_name == 'detail_genre' or url_name == 'all_genres' or url_name == 'all_artists':
        num = 1
    elif url_name == 'favorite_albums':
        num = 2
    elif url_name == 'favorite_musics':
        num = 3
    else:
        num = 0
    return {
        'page': num
    }