from django.db import models

from users.models import Users
from django.core.validators import EmailValidator, URLValidator

# Create your models here.
class NotificationChannel(models.Model):
    
    class TypeChoice(models.TextChoices):
        EMAIL = 'email', 'Mail'
        WEBHOOK = 'webhook', 'Webhook'
        SMS = 'sms', 'SMS'
        SLACK = 'slack', 'Slack'
        TELEGRAM = 'telegram', 'Telegram'
        
    
    name = models.CharField(max_length=100,blank=True,unique=True) 
    notification_type = models.CharField(
        max_length=30,
        choices=TypeChoice.choices,
        default=TypeChoice.EMAIL)
    isSubscribed = models.BooleanField(default=False)
    
    user = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='notification_channels')
    
    def __str__(self) :
        return self.name
    


class EmailNotificationChannel(NotificationChannel):
    email_field = models.EmailField(validators=[EmailValidator])
    
class WebhookNotificationChannel(NotificationChannel):

    webhook_url = models.URLField(validators=[URLValidator])
    
class SMSNotificatonChannel(NotificationChannel):
    sms_field = models.CharField(max_length=30,blank=True)
    
class SlackNotificationChannel(NotificationChannel):
    slack_username = models.CharField(max_length=100,default='Prometheus')
    incoming_webhook = models.URLField(validators=[URLValidator])
    slack_channel = models.CharField(max_length=100)
    
class TelegramNotificationChannel(NotificationChannel):
    tele_webhook = models.URLField(validators=[URLValidator])