from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import verify,verify_email_confirm,verify_channel_confirm, verify_channel

urlpatterns = [
    path('email/<str:token>', csrf_exempt(verify_email_confirm)),
    path('channel/<str:token>', csrf_exempt(verify_channel)),
]
