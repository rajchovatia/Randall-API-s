from django.conf import settings
import jwt

def decode_jwt_token(token):
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        # Extract the user ID from the decoded token's payload
        user_id = decoded_token.get('user_id')
        return user_id
    except jwt.DecodeError:
        # Handle decoding errors
        print("Error decoding JWT token.")
        return None
    