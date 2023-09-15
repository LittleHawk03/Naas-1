from rest_framework import serializers

from .models import Users
from notification_channel.serializers import NotifcationTest, EmailNotificationChannelSerializer, SMSNotificationChannelSerializer, SlackNotificationChannelSerializer, WebhookNotificationChannelSerializer

    


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    notification_channels = NotifcationTest(many=True, read_only=True)
    class Meta:
        model = Users
        fields = [ "id","name", "username", "email", "gender", "location", "date_of_birth"
                  , "account_create_date"
                  , "active"
                  , "notification_channels",]
        # fields = '__all__'

        
        # 0865026026
        

    

     
     
     