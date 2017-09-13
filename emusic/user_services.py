from emusic.error_utils import BusinessError
from emusic.models import Profile
import random, string
from django.contrib.auth import authenticate, login as django_login


class MusicLifeBaseService(object):
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

class MusicLifeSignupService(MusicLifeBaseService):
    def _do_execute(self, **kwargs):
        request = kwargs['request']
        firstname = kwargs['firstname']
        lastname = kwargs['lastname']
        email = kwargs['email']
        gender = kwargs['gender']
        fb_id = kwargs['fb_id']
        fb_name = kwargs['fb_name']
        fb_image = kwargs['fb_image']
        fb_token = kwargs['fb_token']
        profile = kwargs['profile']
        
        if email is not None: 
            username = email
        gen_password = None
        password = self._gen_password()

        error_code = 0
        profile = None

        data = {}
        data['fb_image'] = fb_image

        if profile is None:
            error_code, user, profile = Profile.signup_facebook(username, password, email,
                                                                firstname,lastname, gender, fb_id, data, fb_token)                                              
                          
        else:
            error_code, user, profile = self._update_profile_admin_create(profile=profile,
                                                                          username=username,
                                                                          email=email,
                                                                          password=password,
                                                                          firstname=firstname,
                                                                          lastname=lastname,
                                                                          gender=gender,
                                                                          fb_id=fb_id,
                                                                          data=data_dict,
                                                                          fb_token=fb_token)          
        return error_code, user, profile

    def _update_profile_admin_create(self, **kwargs):
        print '_update_profile_admin_create'
        from django.contrib.auth.models import User
        error_code = 0
        profile = kwargs.get("profile", None)
        user = profile.user
        username = kwargs.get("username", None)
        email = kwargs.get("email", None)
        password = kwargs.get("password", None)
        firstname = kwargs.get("firstname", None)
        lastname = kwargs.get("lastname", None)
        gender = kwargs.get("gender", 0)
        fb_id = kwargs.get("fb_id", None)
        data = kwargs.get("data", {})
        fb_token = kwargs.get("fb_token", None)

        user.set_password(password)

        if username is not None:
            user_username = '%s' % (username)
        else:
            user_username = '%s' % (email)

        user_email = '%s' % (email)

        if User.objects.filter(username=user_username).exists():
            error_code = 1000
            return error_code, None, None

        user.username = user_username
        user.email = user_email

        if firstname is not None or lastname is not None:
            if firstname is not None:
                user.firstname = firstname
            if last_name is not None:
                user.lastname = lastname
        user.save()

        if gender is not None:
            profile.gender = gender

        profile.save()

        return error_code, user, profile


    def _gen_password(self, length=8):
        password = ''.join(
            random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(length))
        return password

