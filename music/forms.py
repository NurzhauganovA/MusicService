from . models import *
from django . forms import *


class CreateMusicForm(ModelForm):
    class Meta:
        model = Music

        fields = ['name_of_song', 'genre', 'music_file', 'cover_image', 'text_of_song']

        labels = {
            'genre': 'Genre of song:',
            'music_file': 'Select music file(.mp3):',
            'cover_image': 'Select music cover image:',
            'text_of_song': 'Lyric of song:'
        }

        widgets = {
            "music_file": FileInput(attrs={
                'class': 'form-control',
            }),
            "cover_image": FileInput(attrs={
                'class': 'form-control',
            }),
            "name_of_song": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name of song'
            }),
            "text_of_song": Textarea(attrs={
                'class': 'form-control',
            }),
        }
