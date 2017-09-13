# -*- coding: utf-8 -*-
from emusic.error_utils import BusinessError

class MusicBaseService(object):
    def execute(self, **kwargs):  # be called from views or test
        self._will_execute(**kwargs)
        try:
            result = self._do_execute(**kwargs)
        except BusinessError:
            self._did_execute_error(**kwargs)
            raise
        except:
            self._did_execute_error_critical(**kwargs)
            raise

        self._did_execute_success(**kwargs)
        return result

    def _will_execute(self, **kwargs):  # used b4 do the main objective
        return None

    def _do_execute(self, **kwargs):  # the main objective must be implemented
        raise NotImplementedError("_do_execute not be implement yet.")

    def _did_execute_error(self, **kwargs):  # used after do the main objective
        # log error
        #LogService().log("error %s" % kwargs)
        return None

    def _did_execute_error_critical(self, **kwargs):  # used after do the main objective
        # log error
        #LogService().log("critical error %s" % kwargs)
        return None

    def _did_execute_success(self, **kwargs):  # used after do the main objective
        # log
        #LogService().log("success %s" % kwargs)
        return None

class MusicListService(MusicBaseService):
    def _do_execute(self, **kwargs):
        from emusic.models import Music
        request = kwargs['request']

        error_code = 0
        list = []
        music_list = Music.objects.all()
        for music in music_list:
            music_item = self.get_music_detail(music)
            list.append(music_item)
        return error_code, list

    def get_music_detail(self, music):       
        music_dict = dict()
        music_dict['music_id'] = music.id
        music_dict['music_name'] = music.music_name
        music_dict['artist_name'] = music.artist_name
        music_dict['album_name'] = music.album_name
        music_dict['genres'] = music.genres
        music_dict['status'] = music.status

        data = music.get_data_json()
        music_dict['music_url'] = data.get('music_url')
        
        image = dict()
        img_url = data.get('image_url', "")
        image['image_url'] = img_url
        if len(img_url) == 0:
            image['status'] = False
        else:
            image['status'] = True
        music_dict['image'] = image

        return music_dict

class FavoriteMusicService(MusicBaseService):
    def _do_execute(self, **kwargs):
        from emusic.models import Favorite, Profile, Music
        request = kwargs['request']
        profile_id = kwargs['profile_id']
        music_id = kwargs['music_id']
        is_active = kwargs['is_active']

        if not Favorite.objects.filter(profile__id=profile_id).exists():
            print 'n'
            fav_music = Favorite(profile__id=profile_id,
                                 music__id=music_id,
                                 is_active=is_active)
            fav_music.save()
        else:
            print 'h'
                        
        