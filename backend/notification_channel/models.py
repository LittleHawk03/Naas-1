from django.db import models

from users.models import Users

# Create your models here.
class NotificationChannel(models.Model):
    
    class TypeChoice(models.TextChoices):
        EMAIL = 'email', 'Mail'
        WEBHOOK = 'webhook', 'Webhook'
        SMS = 'sms', 'SMS' 
        SLACK = 'slack', 'Slack'
    
    # name of notification channel, it can be set or be blank (not require) 
    name = models.CharField(max_length=100,blank=True)
    
    # the unique name (* required because it use for query or select from user) 
    unique_name = models.CharField(max_length=100,unique=True)
    
    # notification type (it can be email,weebhook, sms and slack)
    notification_type = models.CharField(max_length=30,choices=TypeChoice.choices,default=TypeChoice.EMAIL)
    
    # include email address, webhook url, slack webhook url
    receiver_field = models.CharField(max_length=200,null=False)
    
    # slack channel if notification type is slack
    slack_channel = models.CharField(max_length=50,blank=True)
    
    # after verify the "isSubcribed" will be true
    isSubscribed = models.BooleanField(default=False)
    
    user = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='notification_channel')
    
    # @property
    # def notification_channel(self):
    #     return [
            
    #     ]
    
    def __str__(self) :
        return self.username
