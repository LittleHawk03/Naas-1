from rest_framework import serializers

from .models import Users
# from notification_channel.serializers import NotificationChannelSerializer
# from notification_channel.serializers import NotificationChannelListSerializer
from notification_channel.serializers import NotifcationTest
from notification_channel.models import NotificationChannel

    


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    # id = serializers.IntegerField(read_only=True)
    notification_channel = NotifcationTest(many=True, read_only=True)
    # print(notification_channel)
    class Meta:
        model = Users
        # fields = '__all__' 
        fields = [
            "id",
            "name",
            "username",
            "email",
            "gender",
            "location",
            "date_of_birth",
            "account_create_date",
            "active",
            "notification_channel",
        ]
    

        
        # 0865026026
        

    

     
     
     