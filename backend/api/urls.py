from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import verify_email_page

urlpatterns = [
    path('email/<str:token>', csrf_exempt(verify_email_page)),
]
