from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveUpdateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User, PasswordResetOTP

from .serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    RegisterSerializer,
    RequestOTPSerializer,
    UserProfileSerializer,
)
from .utils import generate_otp, send_otp_email


# Register
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"message": "Пользователь успешно создан!"})


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Пользователь успешно создан!"})


# Login
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.validated_data)


# Logout
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    Token.objects.filter(user=request.user).delete()
    return Response({"message": "Вы успешно вышли!"})


# Delete account
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user
    Token.objects.filter(user=user).delete()
    user.delete()
    return Response({"message": "Аккаунт успешно удалён!"})


# Profile
class ProfileAPIView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


# Change Password
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(
        data=request.data,
        context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(
        {"message": "Пароль успешно изменён!"},
        status=status.HTTP_200_OK
    )


# Request OTP (БЕЗ УЯЗВИМОСТИ)
class RequestOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        # безопасный поиск пользователя (без падения)
        user = User.objects.filter(email=email).first()

        if user:
            # деактивируем старые OTP
            PasswordResetOTP.objects.filter(
                user=user,
                is_used=False
            ).update(is_used=True)

            otp = generate_otp(4)

            PasswordResetOTP.objects.create(
                user=user,
                otp_code=otp
            )

            # защита от падения при отправке email
            try:
                send_otp_email(email, otp)
            except Exception:
                pass  # логировать в проде обязательно

        # одинаковый ответ для всех случаев (защита от перебора email)
        return Response(
            {"message": "Если аккаунт существует, OTP отправлен"},
            status=status.HTTP_200_OK
        )

# Verify OTP
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp_obj = serializer.validated_data['otp_obj']
        otp_obj.is_used = True
        otp_obj.save()
        return Response(
            {"message": "OTP подтверждён"},
            status=status.HTTP_200_OK
        )


# Reset Password
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Пароль успешно изменён"},
            status=status.HTTP_200_OK
        )