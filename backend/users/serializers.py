from rest_framework import serializers

from .models import Users
from notification_channel.serializers import NotifcationTest, EmailNotificationChannelSerializer, SMSNotificationChannelSerializer, SlackNotificationChannelSerializer, WebhookNotificationChannelSerializer

    


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    # notification_channels = NotifcationTest(many=True, read_only=True)
    email_notification_channels = EmailNotificationChannelSerializer(many=True, read_only=True)
    webhook_notification_channels = WebhookNotificationChannelSerializer(many=True, read_only=True)
    sms_notification_channels = SMSNotificationChannelSerializer(many=True,read_only=True)
    slack_notification_channels = SlackNotificationChannelSerializer(many=True,read_only=True)
    class Meta:
        model = Users
        fields = [ "id","name", "username", "email", "gender", "location", "date_of_birth"
                  , "account_create_date"
                  , "active"
                  , "email_notification_channels",
                  "webhook_notification_channels",
                  "sms_notification_channels",
                  "slack_notification_channels",]
    

        
        # 0865026026
        

    

     
     
     