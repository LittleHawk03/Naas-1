from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import NotificationChannel, SMSNotificatonChannel,EmailNotificationChannel,WebhookNotificationChannel,SlackNotificationChannel
from .serializers import NotificationChannelSerializer, NotifcationTest 
from .serializers import EmailNotificationChannelSerializer, WebhookNotificationChannelSerializer, SMSNotificationChannelSerializer,SlackNotificationChannelSerializer
from api.channel_confirm import send_channel



class NotificationChannelCreateView(ModelViewSet):
    queryset = NotificationChannel.objects.all()
    serializer_class = NotificationChannelSerializer
    
    @action(methods=['post'],detail=True)
    def perform_create(self, serializer):
        notification_type = self.request.data.get('notification_type')
        serializer = None
        
        if notification_type == 'email':
            serializer_class = EmailNotificationChannelSerializer
        elif notification_type == 'webhook':
            serializer_class = WebhookNotificationChannelSerializer
        elif notification_type == 'sms':
            serializer_class = SMSNotificationChannelSerializer
        elif notification_type == 'slack':
            serializer_class = SlackNotificationChannel
        else:
            return Response({"detail": "Invalid notification type"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = serializer_class(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response({"some thing be wrong"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
class NotificationChannelListView(ModelViewSet):
    queryset = NotificationChannel.objects.all()
    serializer_class = NotificationChannelSerializer

    def list(self, request, *args, **kwargs):
        email_channels = EmailNotificationChannel.objects.all()
        webhook_channels = WebhookNotificationChannel.objects.all()
        sms_channels = SMSNotificatonChannel.objects.all()
        slack_channels = SlackNotificationChannel.objects.all()

        email_serializer = EmailNotificationChannelSerializer(email_channels, many=True)
        webhook_serializer = WebhookNotificationChannelSerializer(webhook_channels, many=True)
        sms_serializer = SMSNotificationChannelSerializer(sms_channels, many=True)
        slack_serializer = SlackNotificationChannelSerializer(slack_channels, many=True)

        data = {
            "email_channels": email_serializer.data,
            "webhook_channels": webhook_serializer.data,
            "sms_channels": sms_serializer.data,
            "slack_channels": slack_serializer.data,
        }
        
        
        return Response(data)
    
    
class NotificationChannelRetrieveView(ModelViewSet):
    queryset = NotificationChannel.objects.all()
    serializer_class = NotificationChannelSerializer
    
    def retrieve(self, request, *args, **kwargs):
        try:
            object = self.get_object()
            print(object.id)  
            notification_type = object.notification_type
            if notification_type == 'email':
                data = EmailNotificationChannel.objects.get(id=object.id)
                serializer_class = EmailNotificationChannelSerializer(data)
            elif notification_type == 'webhook':
                data = WebhookNotificationChannel.objects.get(id=object.id)
                serializer_class = WebhookNotificationChannelSerializer(data)
            elif notification_type == 'sms':
                data = SMSNotificatonChannel.objects.get(id=object.id)
                serializer_class = SMSNotificationChannelSerializer(data)
            elif notification_type == 'slack':
                data = SlackNotificationChannel.objects.get(id=object.id)
                serializer_class = SlackNotificationChannel(data)
            else:
                return Response({"detail": "Invalid notification type"}, status=status.HTTP_400_BAD_REQUEST)
            # data = EmailNotificationChannel.objects.get(id=object.id)
            # serializer_class = EmailNotificationChannelSerializer(data)    
            return Response(serializer_class.data,status=status.HTTP_200_OK)
        except (ValueError, ObjectDoesNotExist):
            return Response({"detail":"Some thing can be wrong"},status=status.HTTP_200_OK)

        
class NotificationChannelDestroyView(ModelViewSet):
    queryset = NotificationChannel.objects.all()
    serializer_class = NotificationChannelSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        return super(NotificationChannelDestroyView, self).destroy(request, *args, **kwargs)
    
    

    

class NotificationChannelUpdateEmail(ModelViewSet):
    queryset = EmailNotificationChannel.objects.all()
    serializer_class = EmailNotificationChannelSerializer
    
    def perform_update(self, serializer):
        instance = self.get_object()
        serializer.save()
        return super().perform_update(serializer)

class NotificationChannelUpdateWeb(ModelViewSet):
    queryset = WebhookNotificationChannel.objects.all()
    serializer_class = EmailNotificationChannelSerializer
    
    def perform_update(self, serializer):
        instance = self.get_object()
        serializer.save()
        return super().perform_update(serializer)
    
class NotificationChannelUpdateSMS(ModelViewSet):
    queryset = SMSNotificatonChannel.objects.all()
    serializer_class = SMSNotificationChannelSerializer
    
    def perform_update(self, serializer):
        instance = self.get_object()
        serializer.save()
        return super().perform_update(serializer)
    
class NotificationChannelUpdateSlack(ModelViewSet):
    queryset = SlackNotificationChannel.objects.all()
    serializer_class = SlackNotificationChannelSerializer
    
    def perform_update(self, serializer):
        instance = self.get_object()
        serializer.save()
        return super().perform_update(serializer)