from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from .confirm import verify_email_view, verify_email
from .channel_confirm import verify_email_view_channel,verify_email_channel
# , verify_password_view, verify_password
from .errors import NotAllFieldCompiled


@verify_email_view
def verify(request: WSGIRequest, token):
    try:
        template = settings.EMAIL_MAIL_PAGE
        success, user = verify_email(token)
        return render(request, template, {'success': success, 'user': user, 'request': request})
    except (AttributeError, TypeError):
        raise NotAllFieldCompiled('EMAIL_MAIL_PAGE_TEMPLATE field not found')


verify_email_confirm = verify


@verify_email_view_channel
def verify_channel(request: WSGIRequest, token):
    try:
        template = settings.EMAIL_MAIL_PAGE
        print("0.0.0.0")
        success, channel = verify_email_channel(token)
        print(channel.receiver_field)
        return render(request, template, {'success': success, 'user': channel, 'request': request})
    except (AttributeError, TypeError):
        raise NotAllFieldCompiled('EMAIL_MAIL_PAGE_TEMPLATE field not found')
    
verify_channel_confirm = verify_channel