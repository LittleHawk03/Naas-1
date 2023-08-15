from django.db import models

# Create your models here.
class Users(models.Model):
    
    class GenderChoice(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'
        OTHER = 'other',
        
    # class IsActive(models.TextChoices):
        # IsActive = 'T', 'True'
        # IsNotActive = 'F', 'False'
    
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=30,unique=True,null=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=15,choices=GenderChoice.choices,default=GenderChoice.MALE)
    location = models.CharField(max_length=100,blank=True)
    date_of_birth = models.DateField()
    account_create_date = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
    active = models.BooleanField(default=False)
    
    def __str__(self) :
        return self.username