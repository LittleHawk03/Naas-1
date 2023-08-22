from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from .models import Users
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer
from api.confirm import send_email
from django.contrib.auth import get_user_model


       
    
class UserCreateApiView(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    
    def perform_create(self, serializer):
        user = serializer.save()
        
        user_vertifi = Users.objects.get(id=user.id)
        
        send_email(user_vertifi)
        return super().perform_create(serializer)

class UsersListApiView(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get',]
    
    def list(self, request, *args, **kwargs):
        return Response(self.serializer_class(self.queryset, many=True).data
                        ,status=status.HTTP_200_OK)
        
class UserRetrieveApiView(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get',]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object() 
        return Response(self.serializer_class(instance).data,status=status.HTTP_200_OK)
    

class UserUpdateApiView(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['put',]
    
    def perform_update(self, serializer):
        instance = self.get_object()
        serializer.save()
        return super().perform_update(serializer)

class UserDestroyApiView(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['delete',]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        
        return super(UserDestroyApiView, self).destroy(request, *args, **kwargs)

