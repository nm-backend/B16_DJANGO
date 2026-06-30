# Create your views here.

from django.shortcuts import render
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
# Create your views here.


class Register(APIView):
    permission_classes = [AllowAny]  

class Profile(APIView):
    permission_classes = [IsAuthenticated]