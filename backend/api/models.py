from django.db import models

# Create your models here.
class OTPValidation(models.Model):
    
    otp = models.CharField(verbose_name="OTP code",max_length=10)
    phone_number = models.CharField(
        verbose_name="PhoneNumber",
        max_length=30
    )
    create_date = models.DateTimeField(verbose_name="Create Date", auto_now_add=True)
    update_date = models.DateTimeField(verbose_name="Date When Modified", auto_now=True)
    
    is_validated = models.BooleanField(verbose_name="Is Validate",default=False)
    validate_attempt = models.IntegerField(
        verbose_name="Attempted Validation", default=3
    )
    reactive_at = models.DateTimeField(verbose_name="ReActivate Sending OTP") 
    send_counter = models.IntegerField(verbose_name=("OTP Sent Counter"), default=0)
    timeout = models.DateTimeField(verbose_name=("Time out"))
    
    def __str__(self):
        

        return self.phone_number

    class Meta:
       
        verbose_name = "OTP Validation"
        verbose_name_plural = "OTP Validations"