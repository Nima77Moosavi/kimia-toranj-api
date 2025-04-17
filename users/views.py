from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.settings import api_settings
from rest_framework import status
from .serializers import SendOTPSerializer, VerifyOTPSerializer
from .models import User, OTP, BlacklistedAccessToken
from .utils import send_otp


class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            # Generate and send OTP
            send_otp(phone_number)

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
            access = refresh.access_token
            print("PAYLOAD", access.payload)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'is_admin': user.is_staff
            })
        return Response(serializer.errors, status=400)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return Response(
                {"detail": "Authorization header is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            prefix, token = auth_header.split()
            if prefix.lower() != "bearer":
                return Response(
                    {"detail": "Authorization header format must be Bearer <token>."},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            # Decode the token using the configured TokenBackend.
            token_backend = TokenBackend(
                algorithm=api_settings.ALGORITHM,
                signing_key=api_settings.SIGNING_KEY,
            )
            payload = token_backend.decode(token)
            jti = payload.get("jti")
            print("JTI", jti)
            if jti:
                # Add the token’s jti to the blacklist.
                BlacklistedAccessToken.objects.get_or_create(jti=jti)
            return Response(
                {"detail": "Logout successful. This device’s token has now been revoked."},
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {"detail": "Invalid token."},
                status=status.HTTP_401_UNAUTHORIZED
            )
