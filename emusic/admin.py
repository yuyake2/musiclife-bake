from django.contrib import admin
from emusic.models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'email', 'gender', 'timestamp','data', 'fb_image')

class MusicAdmin(admin.ModelAdmin):
    list_display = ('music_name', 'artist_name', 'album_name', 'status','data', 'timestamp')

    
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Music, MusicAdmin)