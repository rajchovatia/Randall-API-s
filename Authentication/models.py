from django.db import models

# Create your models here.

class UserRegistration(models.Model) :
    username = models.CharField(max_length=240, null=True, blank=True)
    email = models.EmailField(max_length=200,null=True,blank=True)
    password = models.CharField(max_length=200,null=True,blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return self.email


