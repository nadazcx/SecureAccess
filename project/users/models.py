from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email=self.normalize_email(email)
        user =self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email,password,**extra_fields)
class CustomUser(AbstractUser):
        cardId=models.CharField(max_length=100)
        objects=CustomUserManager()
        def __str__(self):
            return self.username
