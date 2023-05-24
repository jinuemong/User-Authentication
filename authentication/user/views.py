from django.shortcuts import render
from .models import User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import LoginSerializer,RegistrationSerializer,UserSerializer
from .renderers import UserJsonRenderer
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.generics import RetrieveUpdateAPIView,RetrieveDestroyAPIView



# user Register view 
class RegistrationAPIView(APIView):

    # allow  any
    permission_classes = (AllowAny,)

    serializer_class = RegistrationSerializer
    renderer_classes = (UserJsonRenderer,)

    # post register
    def post(self,request):
        user = request.data 
        