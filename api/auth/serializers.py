from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from users.models import User, PasswordResetOTP


# Registration
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Пароли не совпадают!")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)  
        return user
    

# Login 
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs['email'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("Неверный email или пароль")

        token, _ = Token.objects.get_or_create(user=user)
        return {"token": token.key, "email": user.email}
    

# Profile 
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', "last_name", 'phone_number', "bio",
                  "address", "avatar", "date_joined")
        read_only_fields = ('email',)


# Profile Update
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'bio', 'address', 'avatar')


# Change Password
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(
        write_only=True, 
        validators=[validate_password]
    )

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError(
                "Старый пароль неверный")
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(
            self.validated_data['new_password'])
        user.save()
        return user
    



class RequestOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Пользователь с этим адресом электронной почты не найден."
            )
        return value


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=10)

    def validate(self, attrs):
        email = attrs['email']
        otp = attrs['otp']
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("Неверный email или OTP")
        otp_obj = PasswordResetOTP.objects.filter(
            user=user, otp_code=otp, is_used=False, purpose='password_reset'
        ).order_by('-created_at').first()
        if not otp_obj:
            raise serializers.ValidationError("Неверный OTP")
        attrs['otp_obj'] = otp_obj
        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=10)
    new_password = serializers.CharField(validators=[validate_password])

    def validate(self, attrs):
        email = attrs['email']
        otp = attrs['otp']
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("Неверный email или OTP")
        otp_obj = PasswordResetOTP.objects.filter(
            user=user, otp_code=otp, is_used=False, purpose='password_reset'
        ).first()
        if not otp_obj:
            raise serializers.ValidationError("Неверный OTP")
        attrs['user'] = user
        attrs['otp_obj'] = otp_obj
        return attrs

    def save(self):
        user = self.validated_data['user']
        otp_obj = self.validated_data['otp_obj']
        user.set_password(self.validated_data['new_password'])
        user.save()
        otp_obj.is_used = True
        otp_obj.save()

