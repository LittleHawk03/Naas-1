from django.urls import path,include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'create', views.UserCreateApiView,basename='UserCreateApiView')
router.register(r'retrieve', views.UserRetrieveApiView,basename='UserRetrieveApiView')
router.register(r'lists', views.UsersListApiView,basename='UsersListApiView')
router.register(r'destroy', views.UserDestroyApiView,basename='UserDestroyApiView')
router.register(r'update', views.UserUpdateApiView, basename='UserUpdateApiView')


urlpatterns = [
    path("",include(router.urls)),
]