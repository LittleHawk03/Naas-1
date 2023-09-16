from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
import consul
from .models import NotificationChannel, SMSNotificatonChannel,EmailNotificationChannel,WebhookNotificationChannel,SlackNotificationChannel, TelegramNotificationChannel
from .serializers import NotificationChannelSerializer, NotifcationTest 
from .serializers import EmailNotificationChannelSerializer, WebhookNotificationChannelSerializer, SMSNotificationChannelSerializer,SlackNotificationChannelSerializer, TeleNotificationChannelSerializer
from api.channel_confirm import send_channel
from api.utils import send_vertification_sms



class NotificationChannelCreateView(ModelViewSet):
    queryset = NotificationChannel.objects.all()
    serializer_class = NotificationChannelSerializer
    
    def put_consul_kv(self, notification_channel): 
        consul_host = "116.103.226.93"
        consul_port = 8500
        c = consul.Consul(host=consul_host,port=consul_port)
        user_id = notification_channel.user.id
        notification_type = notification_channel.notification_type
        channel_id = notification_channel.id
        if notification_type == 'email':
            email_field = notification_channel.email_field
            c.kv.put(f"users/{ user_id }/alarms/email/{ channel_id }/receiver", email_field)
        elif notification_type == 'webhook':
            webhook_url = notification_channel.webhook_url
            c.kv.put(f"users/{ user_id }/alarms/webhook/{ channel_id }/url", webhook_url)
        elif notification_type == 'sms':
            sms_field = notification_channel.sms_field
            c.kv.put(f"users/{ user_id }/alarms/sms/{ channel_id }/sms_field", sms_field)
        elif notification_type == 'slack':
            incoming_webhook = notification_channel.incoming_webhook
            slack_channel = notification_channel.slack_channel
            slack_username = notification_channel.slack_username
            c.kv.put(f"users/{ user_id }/alarms/slack/{ channel_id }/username", slack_username)
            c.kv.put(f"users/{ user_id }/alarms/slack/{ channel_id }/channel", incoming_webhook)
            c.kv.put(f"users/{ user_id }/alarms/slack/{ channel_id }/api_url", slack_channel)
        elif notification_type == 'telegram':
            tele_webhook = notification_channel.tele_webhook
            c.kv.put(f"users/{ user_id }/alarms/telegram/{ channel_id }/tele_webhook", tele_webhook)
        else:
            return Response({"detail": "Invalid notification type"}, status=status.HTTP_400_BAD_REQUEST)
            
            
        
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
            serializer_class = SlackNotificationChannelSerializer
        elif notification_type == 'telegram':
            serializer_class = TeleNotificationChannelSerializer
        else:
            return Response({"detail": "Invalid notification type"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = serializer_class(data=self.request.data)
        if serializer.is_valid():
            notification_channel = serializer.save()
            # self.put_consul_kv(notification_channel)
            
            if notification_type == 'email':
                vertify_notification_channel = EmailNotificationChannel.objects.get(id=notification_channel.id)
                send_channel(vertify_notification_channel)
            elif notification_type == 'sms':
                vertify_notification_channel = SMSNotificatonChannel.objects.get(id=notification_channel.id)
                send_vertification_sms(vertify_notification_channel)
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
        tele_channels = TelegramNotificationChannel.objects.all()

        email_serializer = EmailNotificationChannelSerializer(email_channels, many=True)
        webhook_serializer = WebhookNotificationChannelSerializer(webhook_channels, many=True)
        sms_serializer = SMSNotificationChannelSerializer(sms_channels, many=True)
        slack_serializer = SlackNotificationChannelSerializer(slack_channels, many=True)
        tele_serializer = TeleNotificationChannelSerializer(tele_channels, many=True)
        
        data = {
            "email_channels": email_serializer.data,
            "webhook_channels": webhook_serializer.data,
            "sms_channels": sms_serializer.data,
            "slack_channels": slack_serializer.data,
            "tele_channels" : tele_serializer.data,
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
                serializer_class = SlackNotificationChannelSerializer(data)
            elif notification_type == 'telegram':
                data = TelegramNotificationChannel.objects.get(id=object.id)
                serializer_class = TeleNotificationChannelSerializer(data)
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
    
    def delete_consul_kv(self, notification_channel):
        consul_host = "116.103.226.93"
        consul_port = 8500
        c = consul.Consul(host=consul_host,port=consul_port)
        user_id = notification_channel.user.id
        channel_id = notification_channel.id
        if notification_channel.notification_type == 'email':
            c.kv.delete(f"users/{ user_id }/alarms/email/{ channel_id }/receiver")
        elif notification_channel.notification_type == 'webhook':
            c.kv.delete(f"users/{ user_id }/alarms/webhook/{ channel_id }/url")
        elif notification_channel.notification_type == 'sms':
            c.kv.delete(f"users/{ user_id }/alarms/sms/{ channel_id }/url")
        elif notification_channel.notification_type == 'slack':
            c.kv.delete(f"users/{ user_id }/alarms/slack/{ channel_id }/username")
            c.kv.delete(f"users/{ user_id }/alarms/slack/{ channel_id }/channel")
            c.kv.delete(f"users/{ user_id }/alarms/slack/{ channel_id }/api_url")
        elif notification_channel.notification_type == 'telegram':
            c.kv.delete(f"users/{ user_id }/alarms/telegram/{ channel_id }/tele_webhook")
        else:
            return Response({"detail": "Invalid notification type"}, status=status.HTTP_400_BAD_REQUEST)        
        
        
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.notification_type == 'email':
            object = EmailNotificationChannel.objects.get(id=instance.id)
            self.delete_consul_kv(object)
        elif instance.notification_type == 'webhook':
            object = WebhookNotificationChannel.objects.get(id=instance.id)
            self.delete_consul_kv(object)
        elif instance.notification_type == 'sms':
            object = SMSNotificatonChannel.objects.get(id=instance.id)
            self.delete_consul_kv(object)
        elif instance.notification_type == 'slack':
            object = SlackNotificationChannel.objects.get(id=instance.id)
            self.delete_consul_kv(object)
        elif instance.notification_type == 'telegram':
            object = TelegramNotificationChannel.objects.get(id=instance.id)
            self.delete_consul_kv(object)
        else:
            return Response({"detail": "Invalid notification type"}, status=status.HTTP_400_BAD_REQUEST)        
        
        return super(NotificationChannelDestroyView, self).destroy(request, *args, **kwargs)
    
    

    

class NotificationChannelUpdateEmail(ModelViewSet):
    queryset = EmailNotificationChannel.objects.all()
    serializer_class = EmailNotificationChannelSerializer
    
    def update_consul_kv(self,notification_channel, object_request):
        consul_host = "116.103.226.93"
        consul_port = 8500
        c = consul.Consul(host=consul_host,port=consul_port)
        user_id = notification_channel.user.id
        channel_id = notification_channel.id
        if notification_channel.notification_type == 'email':
            email_field = object_request['email_field']
            c.kv.put(f"users/{ user_id }/alarms/email/{ channel_id }/receiver", email_field)
        elif notification_channel.notification_type == 'webhook':
            webhook_url = object_request['webhook_url']
            c.kv.put(f"users/{ user_id }/alarms/webhook/{ channel_id }/url", webhook_url)
        elif notification_channel.notification_type == 'sms':
            sms_field = object_request['sms_field']
            c.kv.put(f"users/{ user_id }/alarms/sms/{ channel_id }/url", sms_field)
        elif notification_channel.notification_type == 'slack':
            incoming_webhook = object_request['incoming_webhook']
            slack_channel = object_request['slack_channel']
            slack_username = object_request['slack_username']
            c.kv.put(f"users/{ user_id }/alarms/slack/{ channel_id }/username", slack_username)
            c.kv.put(f"users/{ user_id }/alarms/slack/{ channel_id }/channel", incoming_webhook)
            c.kv.put(f"users/{ user_id }/alarms/slack/{ channel_id }/api_url", slack_channel)
        elif notification_channel.notification_type == 'telegram':
            tele_webhook = notification_channel.tele_webhook
            c.kv.put(f"users/{ user_id }/alarms/telegram/{ channel_id }/tele_webhook", tele_webhook)
        else:
            return Response({"detail": "Invalid notification type"}, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_update(self, serializer):
        instance = self.get_object()
        # print(instance.email_field)
        # print(self.request.data['email_field'])
        object = self.request.data
        self.update_consul_kv(instance,object)
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