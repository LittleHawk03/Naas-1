from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from .serializers import OTPVertificationSerializer
from .confirm import verify_email_view, verify_email
from notification_channel.models import NotificationChannel
from notification_channel.models import SMSNotificatonChannel
from .channel_confirm import verify_email_view_channel,verify_email_channel
# , verify_password_view, verify_password
from .errors import NotAllFieldCompiled
from rest_framework.views import APIView
from .utils import validate_otp
from .utils import generate_otp
from .utils import send_otp
from .utils import send_message
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from notification_channel.consulkv import put_consul_kv

@verify_email_view
def verify(request: WSGIRequest, token):
    try:
        template = settings.EMAIL_MAIL_PAGE
        success, user = verify_email(token)
        return render(request, template, {'success': success, 'user': user, 'request': request})
    except (AttributeError, TypeError):
        raise NotAllFieldCompiled('EMAIL_MAIL_PAGE_TEMPLATE field not found')


verify_email_confirm = verify


@verify_email_view_channel
def verify_channel(request: WSGIRequest, token):
    try:
        template = settings.EMAIL_CHANNEL_PAGE
        success, channel = verify_email_channel(token)
        print(channel.email_field)
        return render(request, template, {'success': success, 'user': channel, 'request': request})
    except (AttributeError, TypeError):
        raise NotAllFieldCompiled('EMAIL_CHANNEL_PAGE_TEMPLATE field not found')
    
verify_channel_confirm = verify_channel


class OTPVerificationView(APIView):
    
    serializer_class = OTPVertificationSerializer
    
    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        name = serializer.validated_data.get("name")
        phone_number = serializer.validated_data.get("phone_number")
        verify_otp = serializer.validated_data.get("verify_otp")
        notificationChannel = serializer.validated_data.get("notificationchannel")
        
        # otp_obj_phone = generate_otp(phonenumber=phone_number)
        # print(otp_obj_phone.otp)
        # test = validate_otp(phone_number=phone_number,otp=otp_obj_phone.otp)
        # message_send = send_message(message="your OTP: " + otp_obj_phone.otp,phone_number="+84349354228")
        
        
        if verify_otp:
            if validate_otp(phone_number=phone_number, otp= verify_otp):
                channel = SMSNotificatonChannel.objects.get(sms_field=phone_number)
                channel.isSubscribed = True
                channel.save()
                put_consul_kv(channel)
                
                res = {
                    "message" : "the notification channel is subscribed"
                }
                
                return Response(res, status=status.HTTP_200_OK)
        else:
            otp_obj_phone = generate_otp(phonenumber=phone_number)
            
            sentotp_phone = send_otp(phonenumber=phone_number,otpobj=otp_obj_phone)
            
            message = {}
            
            if sentotp_phone["success"]:
                otp_obj_phone.send_counter += 1
                otp_obj_phone.save()
                message["mobile"] = {"otp": ("OTP has been sent successfully.")}
            else:
                message["mobile"] = {
                    "otp": (f'OTP sending failed {sentotp_phone["message"]}')
                }

            if sentotp_phone["success"]:
                curr_status = status.HTTP_201_CREATED
            else:
                raise APIException(
                    detail=("A Server Error occurred: " + sentotp_phone["message"])
                )

            return Response(data=message,status=curr_status)