from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime,timedelta


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    expiry_time = datetime.now() + timedelta(days = 1000)
    expiry_timestamp = int(expiry_time.timestamp())
    refresh.payload['exp'] = expiry_timestamp
    return {
        # 'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
    