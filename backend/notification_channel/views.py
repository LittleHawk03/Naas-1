from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import NotificationChannel
from .serializers import NotificationChannelSerializer, NotificationChannelListSerializer, NotificationPublicSerializer
from .serializers import NotificationCreateSerializer


class NotificationCreatAPIView(generics.CreateAPIView):
    queryset = NotificationChannel.objects.all()
    serializer_class = NotificationChannelSerializer
    
    def perform_create(self, serializer):
        serializer.save()
        return super().perform_create(serializer)
    

# class NotificationCreatAPIView2(generics.CreateAPIView):
#     queryset = NotificationChannel.objects.all()
#     serializer_class = NotificationCreateSerializer
    
#     def perform_create(self, serializer):
#         serializer.save()
#         return super().perform_create(serializer)

class NotificationDetailAPIView(generics.RetrieveAPIView):
    queryset = NotificationChannel.objects.all()
    serializer_class = NotificationChannelListSerializer
    

class NotificationListAllAPIView(generics.ListCreateAPIView):
    queryset = NotificationChannel.objects.all()
    serializer_class = NotificationChannelListSerializer
    
class NotificationUpdateAPIView(generics.UpdateAPIView):
    queryset = NotificationChannel.objects.all()
    serializer_class = NotificationChannelSerializer
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        serializer.save()
        return super().perform_update(serializer)
    
    
class NotificationTestAPIView(generics.ListCreateAPIView):
    queryset = NotificationChannel.objects.all()
    serializer_class = NotificationPublicSerializer
    
    
class NotificationDestroyAPIView(generics.DestroyAPIView):
    queryset = NotificationChannel.objects.all()
    serializer_class = NotificationChannelSerializer
    lookup_field = 'pk'
    
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)
    