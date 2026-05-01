from django.urls import path

from . import views

urlpatterns = [
    # Регистрация
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('register/request-otp/', views.RequestRegistrationOTPView.as_view(), name='register-request-otp'),
    path('register/verify-otp/', views.VerifyRegistrationOTPView.as_view(), name='register-verify-otp'),
    path('register/complete/', views.CompleteRegistrationView.as_view(), name='register-complete'),
    
    # Аутентификация
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    # Профиль и аккаунт
    path('profile/', views.ProfileAPIView.as_view(), name='profile'),
    path('change-password/', views.change_password, name='change-password'),
    path('delete-account/', views.delete_account, name='delete-account'),
    
    # Сброс пароля
    path('request-otp/', views.RequestOTPView.as_view(), name='request-otp'),
    path('verify-otp/', views.VerifyOTPView.as_view(), name='verify-otp'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
]
