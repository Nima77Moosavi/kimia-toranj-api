import random
from django.utils import timezone
from .models import OTP

def send_otp(phone_number):
    code = ''.join(random.choices('0123456789', k=6))
    expires_at = timezone.now() + timezone.timedelta(minutes=2)
    
    otp = OTP.objects.create(phone_number=phone_number, code=code, expires_at=expires_at)
    
    print(f"OTP for {phone_number}: {code}")

    return otp