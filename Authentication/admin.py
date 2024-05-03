from django.contrib import admin
from Authentication.models import UserRegistration
# Register your models here.


@admin.register(UserRegistration)
class UserAdmin(admin.ModelAdmin) :
    list_display = ['username','email','profile_image']
    
    
    