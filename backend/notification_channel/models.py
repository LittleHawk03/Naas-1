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
        
    
    # name = models.CharField(max_length=100,blank=True,unique=True) 
    notification_type = models.CharField(
        max_length=30,
        choices=TypeChoice.choices,
        default=TypeChoice.EMAIL)
    isSubscribed = models.BooleanField(default=False)
    
    
    
    def __str__(self) :
        return self.username
    
    # class Meta:
    #     abstract = True


class EmailNotificationChannel(models.Model):
    user = GenericRelation(Users,content_type_field='user_content_type',object_id_field='id')
    email_field = models.EmailField(validators=[EmailValidator])
    
class WebhookNotificationChannel(models.Model):
    user = GenericRelation(Users,content_type_field='user_content_type',object_id_field='id')
    webhook_url = models.URLField(validators=[URLValidator])
    
class SMSNotificatonChannel(models.Model):
    user = GenericRelation(Users,content_type_field='user_content_type',object_id_field='id')
    sms_field = models.CharField(max_length=30,blank=True)
    
class SlackNotificationChannel(models.Model):
    user = GenericRelation(Users,content_type_field='user_content_type',object_id_field='id')
    incoming_webhook = models.URLField(validators=[URLValidator])
    slack_channel = models.CharField(max_length=100)
    
