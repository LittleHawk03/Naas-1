import datetime
from typing import Dict
import pytz
from notification_channel.models import NotificationChannel
from .models import OTPValidation
from django.utils import timezone
from django.conf import settings
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import AuthenticationFailed
from twilio.rest import Client
import pyotp



otp_settings = {
    "LENGTH": 5,
    "ALLOWED_CHARS": "1234567890",
    "VALIDATION_ATTEMPTS": 3,
    "SUBJECT": "OTP for Verification",
    "COOLING_PERIOD": 3,
}

def send_vertification_sms(notification_channel):
    phone_number = notification_channel.sms_field
    otp_obj = generate_otp(phonenumber=phone_number)
    print("step-sms-1")
    send_otp(phonenumber=phone_number,otpobj=otp_obj)

def datetime_passed_now(source: datetime.datetime) -> bool:
    """
    Compares provided datetime with current time on the basis of Django
    settings. Checks source is in future or in past. False if it's in future.
    Parameters
    ----------
    source: datetime object than may or may not be naive

    Returns
    -------
    bool

    Author: Himanshu Shankar (https://himanshus.com)
    """
    if source.tzinfo is not None and source.tzinfo.utcoffset(source) is not None:
        return source <= datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    else:
        return source <= datetime.datetime.now()

def generate_otp(phonenumber: str):
    
    # random_number: str = NotificationChannel.objects.make_random_password(
    #     length=otp_settings["LENGTH"], allowed_chars=otp_settings["ALLOWED_CHARS"]
    # )
    
    secret_key = pyotp.random_base32()
    
    random_otp = pyotp.TOTP(secret_key)
    
    random_number: str = random_otp.now()
    
    while OTPValidation.objects.filter(otp__exact=random_number).filter(is_validated=False):
        # random_number: str = NotificationChannel.objects.make_random_password(length=otp_settings["LENGTH"]
                            # , allowed_chars=otp_settings["ALLOWED_CHARS"])
        random_number: str = random_otp.now()
    
    try:
        otp_object: OTPValidation = OTPValidation.objects.get(phone_number=phonenumber)
    except OTPValidation.DoesNotExist:
        otp_object: OTPValidation = OTPValidation()
        otp_object.phone_number = phonenumber
    else:
        if not datetime_passed_now(otp_object.reactive_at):
            return otp_object
    
    otp_object.otp = random_number
    otp_object.is_validated = False
    otp_object.validate_attempt = otp_settings["VALIDATION_ATTEMPTS"]
    
    otp_object.validate_attempt = otp_settings["VALIDATION_ATTEMPTS"]

    otp_object.reactive_at = timezone.now() - datetime.timedelta(minutes=1)
    otp_object.save()
    return otp_object

def send_otp(phonenumber: str, otpobj: OTPValidation, recip: str = None) -> Dict:
    """
    This function sends OTP to specified phonenumber.
    Parameters
    ----------
    phonenumber: str
        This is the phonenumber at which and for which OTP is to be sent.
    otpobj: OTPValidation
        This is the OTP or One Time Passcode that is to be sent to user.
    recip: str
        This is the recipient to whom EMail is being sent. This will be
        deprecated once SMS feature is brought in.

    Returns
    -------

    """
    otp: str = otpobj.otp

    if not datetime_passed_now(otpobj.reactive_at):
        raise PermissionDenied(
            detail=f"OTP sending not allowed until: {otpobj.reactive_at}"
        )

    message = (
        f"OTP for verifying : {phonenumber} is {otp}."
        f"  Don't share this with anyone!"
    )

    try:
        rdata: dict = send_message(message, phonenumber, [recip])
        print("step-sms-1-send")
        
    except ValueError as err:
        raise APIException(f"Server configuration error occurred: {err}")

    otpobj.reactive_at = timezone.now() + datetime.timedelta(
        minutes=otp_settings["COOLING_PERIOD"]
    )
    otpobj.save()
    print("step-sms-2")
    return rdata

def validate_otp(phone_number: str, otp: int) -> bool:
    
    try:
        # Try to get OTP Object from Model and initialize data dictionary
        otp_object: OTPValidation = OTPValidation.objects.get(
            phone_number=phone_number, is_validated=False
        )
    except OTPValidation.DoesNotExist:
        raise NotFound(
            detail=(
                "No pending OTP validation request found for provided "
                "phone_number. Kindly send an OTP first"
            )
        )
    # Decrement validate_attempt
    otp_object.validate_attempt -= 1

    if str(otp_object.otp) == str(otp):
        # match otp
        otp_object.is_validated = True
        otp_object.save()
        return True

    elif otp_object.validate_attempt <= 0:
        # check if attempts exceeded and regenerate otp and raise error
        generate_otp(phone_number)
        raise AuthenticationFailed(
            detail=("Incorrect OTP. Attempt exceeded! OTP has been reset.")
        )

    else:
        # update attempts and raise error
        otp_object.save()
        raise AuthenticationFailed(
            detail=(
                f"OTP Validation failed! {otp_object.validate_attempt} attempts left!"
            )
        )
     

def send_message(message, phone_number, recip = None):
    
    account_sid = settings.TWILIO_SID
    token = settings.TWILIO_TOKEN
    sender = settings.TWILIO_SENDER
    
    twilio_client = Client(account_sid,token)
    
    
    message_respone = twilio_client.messages.create(body=message,to=phone_number,from_=sender)
    
    print (message_respone)
    
    return message_respone