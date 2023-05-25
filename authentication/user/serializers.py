from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
# Serializer for user register
# request + response -> serialize

# register 
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length = 64,
        min_length = 4,
        write_only = True
    )

    class Meta:
        model = User
        fields =[
            'username',
            'password'
        ]
    
    def create(self, validated_data):
        username = validated_data['username']
        if username == 'superuser':
            print("superuser is created ",username)
            return User.objects.create_superuser(**validated_data)
        else:
            return User.objects.create_user(**validated_data)


# Login
# get username + password 
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 64)
    password = serializers.CharField(max_length = 64, write_only = True)
    last_login = serializers.CharField(max_length = 128, read_only = True)

    # validation
    def validate(self, data):
        username = data.get('username',None)
        password = data.get('password',None)

        if username is None:
            raise serializers.ValidationError(
                'An username is required to log in !'
            )
        
        if password is None:
            raise serializers.ValidationError(
                'An password is required to log in '
            )
        
        user = authenticate(username=username,password=password)

        # find user data -> id,pw 
        if user is None:
            raise serializers.ValidationError(
                'An user with this username or pw was not found'
            )
        
        # find un activated user
        if not user.is_active:
            raise serializers.ValidationError(
                'this user has been deactivated'
            )
        
        last_login = timezone.now()
        user.last_login = last_login
        user.save(update_fields=['last_login'])
        return {
            'username':user.username,
            'last_login' : user.last_login
        }


# user Update or user confirmation
class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length = 64,
        min_length = 8,
        write_only = True
    )

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'token'
        ]

        # token : read_only_fields, no entry
        read_only_fields= ('token',)

    # user update function
    def update(self,instance,validated_data):

        # pw -> djnago inner function
        # Pop after use: Increased security
        password = validated_data.pop('password',None)

        for (key,value) in validated_data.items():
            setattr(instance,key,value)
        
        # update pw
        if password is not None:
            # set_password : django inner function
            instance.set_password(password)
        
        # instance : user object
        # save : save in database
        instance.save()
        # return save object
        return instance

    

