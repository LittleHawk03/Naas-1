from datetime import datetime

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from users.models import Users
from notification_channel.models import NotificationChannel, EmailNotificationChannel

class EmailVerificationTokenGeneral():
    '''
        THIS CLASS IS USING FOR GENERAL A TOKEN ANG CHECK THE TOKEN IS MAPPING WHEN VERIFICATION
    '''
    
    secret = settings.SECRET_KEY

    def gen_token(self, obj, expiry,kind, **kwargs):

        exp = int(expiry.timestamp()) if isinstance(expiry, datetime) else expiry
        print("gen token " + kind)
        if kind == 'MAIL':
            
            payload = {'email' : obj.email, 'exp': exp}
        if kind == 'CHANNEL':
            print("1-----------------------1------------------1")
            print(obj.id)
            payload = {'email' : obj.email_field, 'exp': exp}
        
        payload.update(**kwargs)
        return jwt.encode(payload, self.secret , algorithm='HS256'), datetime.fromtimestamp(exp)
        
    
    def check_token(self, token, kind ,**kwargs):
        try:
            payload = jwt.decode(token, self.secret, algorithms='HS256')
            email, exp = payload['email'], payload['exp']
            for k , v in kwargs.items():
                if payload[k]  != v:
                    return False, None
        
            if hasattr(settings, 'EMAIL_MULTI_USER') and settings.EMAIL_MULTI_USER:
                if kind == 'MAIL':
                    obj = Users.objects.filter(email=email)
                if kind == 'CHANNEL':
                    obj = EmailNotificationChannel.objects.filter(email_field=email)
            else:
                if kind == 'MAIL':
                    print(email)
                    obj = [Users.objects.get(email=email)]
                if kind == 'CHANNEL':
                    obj = [EmailNotificationChannel.objects.get(email_field=email)]
        except (ValueError, get_user_model().DoesNotExist, jwt.DecodeError, jwt.ExpiredSignatureError, jwt.ExpiredSignatureError):
            return False, None        
        
        if not len(obj) or obj[0] is None:
            return False, None
        
        return True, obj[0]        
        
        # except (ValueError, get_user_model().DoesNotExist, jwt.DecodeError):
        if not len(obj) or obj[0] is None:
            return False, None

        return True, obj[0]
        
    @staticmethod
    def now():
        return datetime.now().timestamp()
    
default_token_generator = EmailVerificationTokenGeneral()
