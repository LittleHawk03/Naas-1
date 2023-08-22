from django.urls import path, include

from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'lists', views.NotificationChannelListView)
router.register(r'create', views.NotificationChannelCreateView)
router.register(r'retrieve', views.NotificationChannelRetrieveView)
router.register(r'destroy', views.NotificationChannelDestroyView)


router_update = routers.DefaultRouter()
router_update.register(r'email', views.NotificationChannelUpdateEmail)
router_update.register(r'webhook', views.NotificationChannelUpdateWeb)
router_update.register(r'sms', views.NotificationChannelUpdateSMS)
router_update.register(r'slack', views.NotificationChannelUpdateSlack)


urlpatterns = [
    path("", include(router.urls)),
    path("update/", include(router_update.urls))
]