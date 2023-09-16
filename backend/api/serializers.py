from rest_framework import serializers
from notification_channel.models import NotificationChannel,SMSNotificatonChannel


class OTPVertificationSerializer(serializers.Serializer):
    
    name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    verify_otp = serializers.CharField(default=None, required=False)
    
    @staticmethod
    def get_notificationChannel(phone_number: str):
        
        try:
            notificationchannel = SMSNotificatonChannel.objects.get(sms_field=phone_number)
        except SMSNotificatonChannel.DoesNotExist:
            notificationchannel = None

        if notificationchannel:
            if notificationchannel.sms_field != phone_number:
                raise serializers.ValidationError(
                    (
                        "Your account is registered with does not has "
                        "{mobile} as registered mobile. Please login directly via "
                        "OTP with your mobile.".format(mobile=phone_number)
                    )
                )
        return notificationchannel