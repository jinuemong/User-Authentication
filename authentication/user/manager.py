from django.contrib.auth.models import BaseUserManager

# BaseUserManager : DRF 내의 user 생성 시 사용하는 헬퍼 클래스
# create_user
# create_superuser
# is_superuser, is_staff

class UserManageer(BaseUserManager):

    def create_user(self,username,password=None,**extra_fields):

        if username is None:
            raise TypeError("Users must have username")
        
        if password is None:
            raise TypeError("Users must have password")
        
        user = self.model(
            username = username,
            **extra_fields
        ) # pass is hide

        # only pass funtion
        user.set_password(password)

        # save user
        user.save()
        return user
    

    def create_superuser(self,username,password,**extra_fields):

        if password is None:
            raise TypeError("Superuser must have password!")
        
        # create_user -> superuser
        user = self.create_user(username,password,**extra_fields)
        # make superuser
        user.is_superuser = True
        user.is_staff = True
        user.save()
        
        return user
