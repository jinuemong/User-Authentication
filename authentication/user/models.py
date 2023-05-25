from django.db import models
from datetime import datetime,timedelta
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.fields import BooleanField
from .manager import UserManageer

# user model 
class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=64,unique=True,db_column="username")
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=True)

    USERNAME_FIELD = "username" #Log in ID

    objects = UserManageer()

    def __str__(self):
        return self.username
    
    
