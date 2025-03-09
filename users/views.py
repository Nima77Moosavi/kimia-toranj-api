from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SendOTPSerializer, VerifyOTPSerializer
from .models import User, OTP
from .utils import generate_otp


class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            # Generate and send OTP
            generate_otp(phone_number)

            return Response({"message": "OTP sent successfully."})
        return Response(serializer.errors, status=400)


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            code = serializer.validated_data['code']

            try:
                otp_obj = OTP.objects.filter(
                    phone_number=phone_number, code=code).latest('created_at')
                if not otp_obj.is_valid():
                    return Response({"message": "OTP has expired."}, status=400)
            except OTP.DoesNotExist:
                return Response({"message": "Invalid OTP."}, status=400)

            user, created = User.objects.get_or_create(
                phone_number=phone_number)

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'is_admin': user.is_staff
            })
        return Response(serializer.errors, status=400)
