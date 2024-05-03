from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import UntypedToken, TokenError
from .models import UserRegistration

class CustomJWTAuthentication(BaseAuthentication):
       def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            raise AuthenticationFailed('JWT Token Required')

        try:
            token = authorization_header.split()[1]
            decoded_token = UntypedToken(token)
            user_id = decoded_token['user_id']
            user = UserRegistration.objects.get(id=user_id)
            return user, None
        except (TokenError, UserRegistration.DoesNotExist, IndexError):
            raise AuthenticationFailed('Invalid JWT token') 
 
