from rest_framework import serializers
from .models import User, OTP

class SendOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
        
class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6)