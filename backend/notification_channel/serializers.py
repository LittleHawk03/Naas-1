from rest_framework import serializers

from .models import NotificationChannel, EmailNotificationChannel, WebhookNotificationChannel, SlackNotificationChannel, SMSNotificatonChannel, TelegramNotificationChannel


class NotificationChannelSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = NotificationChannel
        fields = [
            "name","notification_type","isSubscribed",
        ]


    
class EmailNotificationChannelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EmailNotificationChannel
        fields = ["id","name","notification_type","isSubscribed","email_field","user"]
        
        
class WebhookNotificationChannelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WebhookNotificationChannel
        fields = ["id","name","notification_type","isSubscribed","webhook_url","user"]

class SMSNotificationChannelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SMSNotificatonChannel 
        fields = ["id","name","notification_type","isSubscribed","sms_field","user"]
        
        
class SlackNotificationChannelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SlackNotificationChannel
        fields = ["id","name","notification_type","isSubscribed","incoming_webhook","slack_channel","user"]


class TeleNotificationChannelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TelegramNotificationChannel
        fields = ["id","name","notification_type","isSubscribed","tele_webhook","user"]



class NotifcationTest(serializers.ModelSerializer):
    class Meta:
        model = NotificationChannel
        fields = '__all__'