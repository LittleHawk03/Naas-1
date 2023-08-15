from rest_framework import serializers

from .models import NotificationChannel


class UserPublicSerializers(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)

class NotificationChannelSerializer(serializers.ModelSerializer):
   
    receiver_field = serializers.CharField(write_only=True)
    
    class Meta:
        model = NotificationChannel
        # fields = '__all__' 
        fields = [
            "name",
            "unique_name",
            "notification_type",
            "receiver_field",
            "slack_channel",
            "isSubscribed",
            "user",
            # "owner",
        ]

class NotificationCreateSerializer(serializers.ModelSerializer):
   
    receiver_field = serializers.CharField(write_only=True)
    
    class Meta:
        model = NotificationChannel
        # fields = '__all__' 
        fields = [
            "name",
            "unique_name",
            "notification_type",
            "receiver_field",
            "slack_channel",
            "isSubscribed",
            "user",
            # "owner",
        ]

class NotificationChannelListSerializer(serializers.ModelSerializer):
    # user = UserSerializer(source='Users',read_only=True)
    receiver_field = serializers.CharField(write_only=True)
    owner = UserPublicSerializers(source='user',read_only=True)
    # notification_channel = NotificationChannelSerializer(many=True)
   
    class Meta:
        model = NotificationChannel
        # fields = '__all__' 
        fields = [
            "name",
            "unique_name",
            "notification_type",
            "receiver_field",
            "slack_channel",
            "isSubscribed",
            # "user",
            "owner",
        ]




class NotificationInlineSericalizer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    unique_name = serializers.CharField(read_only=True)
    # user = serializers.IntegerField(read_only=True)
    


class NotificationPublicSerializer(serializers.Serializer):

    user_notification = serializers.SerializerMethodField(read_only=True)


    def get_user_notification(self, obj):
        # print(obj.id)
        user_id = obj.user.id
        # print(user_id)
        notification = NotificationChannel.objects.filter(id=user_id)
        # notification = NotificationChannel.objects.all()
        # print(notification)
        return NotificationInlineSericalizer(notification, many=True).data
        # return []
        
        
class NotifcationTest(serializers.ModelSerializer):
    class Meta:
        model = NotificationChannel
        fields = '__all__'