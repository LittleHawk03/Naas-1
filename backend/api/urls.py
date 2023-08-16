from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import verify,verify_email_confirm

urlpatterns = [
    path('email/<str:token>', csrf_exempt(verify_email_confirm)),
]
