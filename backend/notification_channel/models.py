from django.db import models
from users.models import Users
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import EmailValidator, URLValidator

# Create your models here.
class NotificationChannel(models.Model):
    
    class TypeChoice(models.TextChoices):
        EMAIL = 'email', 'Mail'
        WEBHOOK = 'webhook', 'Webhook'
        SMS = 'sms', 'SMS'
        SLACK = 'slack', 'Slack'
        
    
    name = models.CharField(max_length=100,blank=True,unique=True) 
    notification_type = models.CharField(
        max_length=30,
        choices=TypeChoice.choices,
        default=TypeChoice.EMAIL)
    isSubscribed = models.BooleanField(default=False)
    
    nc_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    
    def __str__(self) :
        return self.username
    
    # class Meta:
    #     abstract = True


class EmailNotificationChannel(NotificationChannel):
    user = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='email_notification_channels')
    email_field = models.EmailField(validators=[EmailValidator])
    
class WebhookNotificationChannel(NotificationChannel):
    user = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='webhook_notification_channels')
    webhook_url = models.URLField(validators=[URLValidator])
    
class SMSNotificatonChannel(NotificationChannel):
    user = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='sms_notification_channels')
    sms_field = models.CharField(max_length=30,blank=True)
    
class SlackNotificationChannel(NotificationChannel):
    user = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='slack_notification_channels')
    incoming_webhook = models.URLField(validators=[URLValidator])
    slack_channel = models.CharField(max_length=100)
    
