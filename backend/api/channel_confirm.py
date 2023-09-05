import functools
import logging
from threading import Thread
from typing import Callable

import deprecation
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail, BadHeaderError
from django.template import Template, Context
from django.template.loader import render_to_string
from django.urls import get_resolver
from django.utils import timezone

from .errors import InvalidUserModel, NotAllFieldCompiled
from .token import default_token_generator

from django.http import HttpResponse, HttpResponseRedirect


logger = logging.getLogger('django_email_verification')
DJANGO_EMAIL_VERIFICATION_MORE_VIEWS_ERROR = 'ERROR: more than one verify view found'
DJANGO_EMAIL_VERIFICATION_NO_VIEWS_INFO = 'INFO: no verify view found'
DJANGO_EMAIL_VERIFICATION_NO_PARAMETER_WARNING = 'WARNING: found verify view without parameter'


# func.django_email_verification_mail_view_id = True

def send_channel(channel, thread=True, expiry=None):
    print("step-0")
    send_inner(channel, thread, expiry, 'CHANNEL')

def send_inner(channel, thread, expiry, kind):
    try:
        channel.save()


        exp = expiry if expiry is not None else _get_validated_field(f'EMAIL_MAIL_TOKEN_LIFE', 'EMAIL_TOKEN_LIFE',
                                                                     default_type=int) + default_token_generator.now()
        token, expiry = default_token_generator.gen_token(channel, exp, kind=kind)
        
        print("___________________________----------------------_____________________")
        
        # print(channel.email_field)
        sender = _get_validated_field('EMAIL_FROM_ADDRESS')
        domain = _get_validated_field('CHANNEL_PAGE_DOMAIN')
        subject = _get_validated_field(f'EMAIL_CHANNEL_SUBJECT')
        mail_plain = _get_validated_field(f'EMAIL_CHANNEL_PLAIN')
        mail_html = _get_validated_field(f'EMAIL_CHANNEL_HTML')
        # print(channel.email_field)
        
        args = (channel, kind, token, expiry, sender, domain, subject, mail_plain, mail_html)
        if thread:
            t = Thread(target=send_email_thread_2, args=args)
            t.start()
        else:
            print("step1-done")
            send_email_thread_2(*args)
            
    # except AttributeError:
    #     raise InvalidchannelModel('The user model you provided is invalid')
    except NotAllFieldCompiled as e:
        raise e
    except Exception as e:
        logger.info(repr(e))

 

def send_email_thread_2(channel, kind, token, expiry, sender, domain, subject, mail_plain, mail_html):
    domain += '/' if not domain.endswith('/') else ''


    context = {'token': token, 'expiry': expiry, 'channel': channel,'link': domain + token}

   
    context['link'] = domain + token
    
 
    print(context['link'])
   
    subject = Template(subject).render(Context(context))

    text = render_to_string(mail_plain, context)

    html = render_to_string(mail_html, context)
    
    print(channel.email_field)
    
    msg = EmailMultiAlternatives(subject, text, sender, [channel.email_field])

    msg.attach_alternative(html, 'text/html')
    msg.send()
    print("step2-done")


def _get_validated_field(field, fallback=None, default_type=None):
    if default_type is None:
        default_type = str
    try:
        d = getattr(settings, field)
        if d == "" or d is None or not isinstance(d, default_type):
            raise AttributeError
        print("step1.1-done")
        return d
    except AttributeError:
        if fallback is not None:
            return _get_validated_field(field, default_type=default_type)
        raise NotAllFieldCompiled(f"Field {field} missing or invalid")
    

def verify_email_channel(token):
    valid, channel = default_token_generator.check_token(token, kind='CHANNEL')
    # print(channel)
    if valid:
        callback = _get_validated_field('CHANNEL_VERIFIED_CALLBACK', default_type=Callable)
        if hasattr(channel, callback.__name__):
            getattr(channel, callback.__name__)()
        else:
            callback(channel)
        channel.last_login = timezone.now()
        # channel.isSubscribed = True
        print("step-save-done")
        channel.save()
       
        return valid, channel
    return False, None


@deprecation.deprecated(deprecated_in='0.3.0', details='use either verify_email() or verify_password()')
def verify_token(token):
    return verify_email_channel(token)


def verify_email_view_channel(func):
    func.django_email_verification_mail_view_id = True

    @functools.wraps(func)
    def verify_function_wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return verify_function_wrapper

@deprecation.deprecated(deprecated_in='0.3.0', details='use either verify_email_view() or verify_password_view()')
def verify_view_channel(func):
    func.django_email_verification_mail_view_id = True

    @functools.wraps(func)
    def verify_function_wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return verify_function_wrapper