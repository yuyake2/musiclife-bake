from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

MEMBER_GENDER = (
    (0, '-'),
    (1, 'male'),
    (2, 'female'),
)
MUSIC_STATUS = (
    (0, 'active'),
    (1, 'inactive')
)

MUSIC_GENRES = (
    (0, '-'),
    (1, 'hip hop'),
    (2, 'rock'),
    (3, 'classical'),
    (4, 'electronic'),
    (5, 'jazz'),
    (6, 'r&b'),
    (7, 'pop'),
)


class Profile(models.Model):
    id = models.BigIntegerField(primary_key=True, blank=True)
    user = models.ForeignKey('auth.User', related_name='member_user')
    firstname = models.CharField(max_length=512, blank=True)
    lastname = models.CharField(max_length=512, blank=True)
    email = models.CharField(max_length=512, blank=True)
    username = models.CharField(max_length=512, blank=True)
    fb_id = models.BigIntegerField(blank=True,null=True)
    fb_token = models.CharField(max_length=1024, null=True, blank=True, default=None)
    fb_name = models.CharField(max_length=512, blank=True)
    fb_image = models.TextField(blank=True)
    gender = models.IntegerField(choices=MEMBER_GENDER, default=0)
    data = models.TextField(default='null')
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __unicode__(self):
        return '%s' % (self.email)

    def save(self, *args, **kwargs):
        if self._get_pk_val() is None:
            from django.conf import settings
            import time, redis
            redis_server = settings.REDIS_SERVER
            self.id = int('%s%s%s'%(int(time.time()), settings.SERVER_NUM, redis_server.incr('emusic_profile')))
            super(self.__class__, self).save(*args, **kwargs)
        else:
            super(self.__class__, self).save(*args, **kwargs)

    def get_data_json(self, key=None, default=None):
        import json

        try:
            type(self.data_json)
        except:
            try:
                self.data_json = json.loads(self.data)
                if self.data_json is None:
                    self.data_json = {}
            except:
                self.data_json = {}

        if key is not None:
            if key in self.data_json:
                return self.data_json[key]
            else:
                return default

        return self.data_json


    def update_data(self, data_dict):
        import json

        data = self.get_data_json()
        if type(data) == type(None):
            data = {}
        data.update(data_dict)
        self.data = json.dumps(data)

    def get_info(self):
        from django.conf import settings

        result = {}
        result['profile_id'] = self.id
        result['user_id'] = self.user.id
        result['email'] = self.email
        result['firstname'] = self.firstname
        result['lastname'] = self.lastname
        # result['fb_image'] = self.fb_image
        result['fb_token'] = self.fb_token
        result['gender'] = self.gender

        return result

    @staticmethod
    def signup_facebook(username, password, email,firstname,lastname, gender, fb_id, data, fb_token):
        from django.contrib.auth.models import User
        from django.conf import settings
        import datetime

        error_code = 0
        user = None
        profile = None
        using_username = False

        if username is not None and email is not None:
            using_username = True

        user_list = User.objects.filter(username=username)
        
        if user_list.exists():
            user = user_list[0]

        if user is None:
            using_username = False
            user_list = User.objects.filter(email=email)
            if user_list.exists():
                user = user_list[0]

        create_user = (user is None)
        if user is None:
            from django.db import IntegrityError
            try:
                user = User.objects.create_user(username, email, password)
                user.set_password(password)
                user.is_active = True
                user.is_staff = False
                user.is_superuser = False
                user.save()
            except IntegrityError:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    user = User.objects.get(email=email)
        else:
            if user.check_password(password):
                pass
            else:
                 if username is not None and using_username:
                     error_code = 1006
                 else:
                    error_code = 1002   
        if error_code == 0 or (user is None and not Profile.objects.filter(user=user).exists()):
            error_code = 0
            profile_list = Profile.objects.filter(user=user)
            if not profile_list.exists():
                profile = Profile(user=user, 
                                  firstname=firstname,
                                  lastname=lastname, 
                                  email=email,
                                  username=username,
                                  gender=gender, 
                                  fb_id=fb_id,
                                  fb_token=fb_token)
                profile.update_data(data)
                
            else:
                profile = profile_list[0]
                for profile_delete in profile_list[1:]:
                    profile_delete.delete()

            profile.save()
        else:
            error_code = 0
            profile_list = Profile.objects.filter(user=user)

            if len(profile_list)>0:
                profile = profile_list[0]

            
       
        return error_code, user , profile


class Music(models.Model):
    id = models.BigIntegerField(primary_key=True, blank=True)
    music_name = models.CharField(max_length=512, blank=True)
    artist_name = models.CharField(max_length=512, blank=True)
    album_name = models.CharField(max_length=512, blank=True)
    genres = models.IntegerField(choices=MUSIC_GENRES, default=0)
    status = models.IntegerField(choices=MUSIC_STATUS, default=0)
    data = models.TextField(default='null')
    timestamp = models.DateTimeField(auto_now_add=True) 

    def save(self, *args, **kwargs):
        if self._get_pk_val() is None:
            from django.conf import settings
            import time, redis
            redis_server = settings.REDIS_SERVER
            self.id = int('%s%s%s'%(int(time.time()), settings.SERVER_NUM, redis_server.incr('emusic_music')))
            super(self.__class__, self).save(*args, **kwargs)
        else:
            super(self.__class__, self).save(*args, **kwargs)

    def get_data_json(self, key=None, default=None):
        import json

        try:
            type(self.data_json)
        except:
            try:
                self.data_json = json.loads(self.data)
                if self.data_json is None:
                    self.data_json = {}
            except:
                self.data_json = {}

        if key is not None:
            if key in self.data_json:
                return self.data_json[key]
            else:
                return default

        return self.data_json

    def update_data(self, data_dict):
        import json

        data = self.get_data_json()
        if type(data) == type(None):
            data = {}
        data.update(data_dict)
        self.data = json.dumps(data)