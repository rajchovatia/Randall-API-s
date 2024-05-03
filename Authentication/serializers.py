from rest_framework import serializers
from Authentication.models import UserRegistration


class UserRegisterSerializer(serializers.ModelSerializer) :
    
    class Meta :
       model = UserRegistration
       fields = '__all__' 

    