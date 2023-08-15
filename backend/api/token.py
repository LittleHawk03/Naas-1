from datetime import datetime

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from users.models import Users

class EmailVerificationTokenGeneral():
    '''
        THIS CLASS IS USING FOR GENERAL A TOKEN ANG CHECK THE TOKEN IS MAPPING WHEN VERIFICATION
    '''
    
    secret = settings.SECRET_KEY

    def gen_token(self, obj, expiry, **kwargs):
        '''
            Args:
            obj (Model): the obj
            expiry (datetime | int): optional forced expiry date
            kwargs: extra payload for the token

            Returns:
                 (tuple): tuple containing:
                    token (str): the token
                    expiry (datetime): the expiry datetime
        '''
        exp = int(expiry.timestamp()) if isinstance(expiry, datetime) else expiry
        payload = {'email' : obj.email, 'exp': exp}
        payload.update(**kwargs)
        return jwt.encode(payload, self.secret , algorithm='HS256'), datetime.fromtimestamp(exp)
        
    
    def check_token(self, token, **kwargs):
        '''
        '''
        try:
            payload = jwt.decode(token, self.secret, algorithms='HS256')
            email, exp = payload['email'], payload['exp']
            
            for k , v in kwargs.items():
                if payload[k]  != v:
                    return False, None
        
            if hasattr(settings, 'EMAIL_MULTI_USER') and settings.EMAIL_MULTI_USER:
                obj = Users.objects.filter(email=email)
            else:
                obj = [Users.objects.get(email=email)]
        
        except (ValueError, get_user_model().DoesNotExist, jwt.DecodeError, jwt.ExpiredSignatureError, jwt.ExpiredSignatureError):
            return False, None        
        
        # except (ValueError, get_user_model().DoesNotExist, jwt.DecodeError):
        if not len(obj) or obj['0'] is None:
            return False, None
        
    @staticmethod
    def now():
        return datetime.now().timestamp()
    
default_token_generator = EmailVerificationTokenGeneral()
