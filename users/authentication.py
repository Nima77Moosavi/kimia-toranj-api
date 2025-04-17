from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from .models import BlacklistedAccessToken


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        authentication_result = super().authenticate(request)   
        if authentication_result is None:
            return None
        user, validated_token = authentication_result
        jti = validated_token.get('jti')
        if jti and BlacklistedAccessToken.objects.filter(jti=jti).exists():
            raise AuthenticationFailed('Token has been revoked.')
        return (user, validated_token)
