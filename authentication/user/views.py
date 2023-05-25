from django.shortcuts import render
from .models import User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import LoginSerializer,RegistrationSerializer,UserSerializer
from .renderers import UserJsonRenderer
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.generics import RetrieveUpdateAPIView,RetrieveDestroyAPIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status,filters

# user Register view 
class RegistrationAPIView(APIView):

    # allow  any
    permission_classes = (AllowAny,)

    serializer_class = RegistrationSerializer
    renderer_classes = (UserJsonRenderer,)

    # post register
    def post(self,request):
        user = request.data 
        serializer = self.serializer_class(data=user) # serializers
        #validation + exception handling
        serializer.is_valid(raise_exception=True) 
        user =serializer.save() # save

        # token authentication
        # send object  : model
        token = TokenObtainPairSerializer.get_token(user)
        # send refresh + access token 
        refresh_token = str(token)
        access_token = str(token.access_token)

        # return response
        return Response(
            {
                "user" : serializer.data,
                "token": {
                    "access":access_token,
                    "refresh":refresh_token
                }
            },status=status.HTTP_201_CREATED
        )

# Login View
class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJsonRenderer,)
    serializer_class = LoginSerializer

    def post(self,request):
        # find user -> send (serializer)
        user = User.objects.get(username = request.data["username"])

        serializer = self.serializer_class(data=request.data)
        #validation + exception handling
        serializer.is_valid(raise_exception=True) 

        if user is not None: # find user data
            # make token for user
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            # find user -> response 200
            return Response(
                {
                    "user":serializer.data,
                    "token" : {
                        "access" : access_token,
                        "refresh" : refresh_token
                    }
                }, status=status.HTTP_200_OK
            )
        
        else: # not find user data
            return Response(status=status.HTTP_400_BAD_REQUEST)

# search user or user update or delete user
class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView,RetrieveDestroyAPIView):

    # Only authorized users can access
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJsonRenderer,)
    serializer_class = UserSerializer

    # search user
    def get(self,request,*args,**kwargs):
        # return not save
        serializer = self.serializer_class(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    # update patch(part)
    def patch(self, request, *args, **kwargs):
        
        serializer_data = request.data

        # requset.user -> instance
        # serializer_data -> validated_data
        # partial -> partly update
        # Pass data to serializer and receive return
        serializer = self.serializer_class(
            request.user, data = serializer_data, partial = True
        )

        serializer.is_valid(raise_exception=True)

        # save update info and return
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    # delete user 
    def delete(slef,request,*args,**kwargs):
        data = request.data
        user = request.user
        user.delete()
        return Response(data, status=status.HTTP_200_OK)

