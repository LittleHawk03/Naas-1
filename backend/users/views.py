from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Users
from .serializers import UserSerializer

class UserCreatAPIView(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    
    def perform_create(self, serializer):
        name = serializer.validated_data.get('name')
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email') 
        gender = serializer.validated_data.get('gender') 
        location = serializer.validated_data.get('location') 
        date_of_birth = serializer.validated_data.get('date_of_birth') 
        account_create_date = serializer.validated_data.get('account_create_date') 
        active = serializer.validated_data.get('active') 
        if not username:
            username=email
        print(username)
        serializer.save(username=username)
        return super().perform_create(serializer)
    
    
class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    
    
class UserListCreatedAPIView(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    
class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        instance = serializer.save()    
        # return super().perform_update(serializer)

class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)